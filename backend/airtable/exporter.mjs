import Airtable from 'airtable';
import {pathToFileURL} from 'node:url';

export function createBase(apiKey, baseId) {
  return new Airtable({apiKey, endpointUrl: 'https://api.airtable.com',
    noRetryIfRateLimited: true, requestTimeout: 10000}).base(baseId);
}

export async function exportTasks({base, tasks, projectId, tableName,
  sleep = ms => new Promise(resolve => setTimeout(resolve, ms)), now = Date.now, maxDurationMs = 120000}) {
  if (tasks.length > 1000) throw new Error('At most 1000 tasks can be exported.');
  if (new Set(tasks.map(t => t.id)).size !== tasks.length) throw new Error('Duplicate input task IDs.');
  const result = {total: tasks.length, created: 0, updated: 0, failed: 0, failures: []};
  if (!tasks.length) return result;
  const path = '/' + encodeURIComponent(tableName);
  const deadline = now() + maxDurationMs;
  const timeout = () => Object.assign(new Error(), {error: 'EXPORT_TIMEOUT'});
  const fatal = error => [400, 401, 403, 404].includes(error.statusCode) ||
    ['UNKNOWN_FIELD_NAME', 'PUBLIC_API_BILLING_LIMIT_EXCEEDED'].includes(error.error);
  const fail = (batch, error) => {
    let message = 'Airtable is unavailable. Export again to retry this task.';
    if ([401, 403].includes(error.statusCode)) message = 'Airtable credentials do not permit this export.';
    else if (error.statusCode === 404) message = 'The configured Airtable table was not found.';
    else if ([400, 413, 422].includes(error.statusCode)) message = 'Airtable rejected the field values. Check the table schema and task.';
    else if (error.statusCode === 429) message = 'Airtable limit reached. Export again later.';
    else if (error.error === 'EXPORT_TIMEOUT') message = 'Export time limit reached. Export again to retry unfinished tasks.';
    else if (error.error === 'DUPLICATE_TASK_ID') message = 'Multiple Airtable records have this Task ID. Resolve those duplicates first.';
    for (const task of batch) result.failures.push({taskId: task.id, title: task.title, error: message});
    result.failed += batch.length;
  };
  const request = async options => {
    for (let attempt = 0; ; attempt++) {
      if (now() >= deadline) throw timeout();
      // Stay below five calls/second. SDK's unbounded 429 retry is disabled.
      await sleep(250);
      if (now() >= deadline) throw timeout();
      try {
        return await base.makeRequest(options);
      } catch (error) {
        const transient = !fatal(error) && (error.statusCode === 429 ||
          [500, 502, 503, 504].includes(error.statusCode) || error.error === 'CONNECTION_ERROR');
        if (!transient || attempt === 2) throw error;
        const delay = Math.min(60000, (error.statusCode === 429 ? 30000 : 500) * 2 ** attempt);
        if (now() + delay >= deadline) throw timeout();
        await sleep(delay);
      }
    }
  };
  const existing = new Map();
  let offset;
  const offsets = new Set();
  try {
    do {
      const {body} = await request({path, qs: {pageSize: 100, fields: ['Task ID'],
        filterByFormula: `{Project ID}=${JSON.stringify(projectId)}`, ...(offset ? {offset} : {})}});
      for (const record of body.records) {
        const id = record.fields['Task ID'];
        existing.set(id, (existing.get(id) || 0) + 1);
      }
      offset = body.offset;
      if (offset && offsets.has(offset)) throw new Error('Repeated pagination offset');
      offsets.add(offset);
    } while (offset);
  } catch (error) {
    fail(tasks, error);
    return result;
  }
  let abort;
  const writeBatch = async batch => {
    if (abort) { fail(batch, abort); return; }
    try {
      const records = batch.map(task => ({fields: {
        'Task ID': task.id, 'Project ID': projectId, Title: task.title,
        'Task Description': task.description || '', Status: task.status,
        Assignee: task.assignee || '', Position: task.position,
      }}));
      const {body} = await request({method: 'PATCH', path,
        body: {performUpsert: {fieldsToMergeOn: ['Task ID']}, records}});
      const created = body.createdRecords || [], updated = body.updatedRecords || [];
      if (created.length + updated.length !== batch.length) throw new Error('Incomplete Airtable acknowledgement');
      result.created += created.length;
      result.updated += updated.length;
    } catch (error) {
      if (fatal(error) || error.error === 'EXPORT_TIMEOUT') abort = error;
      // A rejected batch does not identify its bad row. Diagnose smaller, new
      // batches; a known permanently rejected single record is never retried.
      if ([413, 422].includes(error.statusCode) && !abort && batch.length > 1) {
        const middle = Math.floor(batch.length / 2);
        await writeBatch(batch.slice(0, middle));
        await writeBatch(batch.slice(middle));
      } else fail(batch, error);
    }
  };
  const eligible = tasks.filter(task => {
    if ((existing.get(task.id) || 0) > 1) {
      fail([task], {error: 'DUPLICATE_TASK_ID'});
      return false;
    }
    return true;
  });
  for (let start = 0; start < eligible.length; start += 10) await writeBatch(eligible.slice(start, start + 10));
  return result;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    let input = '';
    for await (const chunk of process.stdin) input += chunk;
    const {tasks, projectId} = JSON.parse(input);
    const apiKey = process.env.AIRTABLE_API_KEY, baseId = process.env.AIRTABLE_BASE_ID;
    const tableName = process.env.AIRTABLE_TABLE_NAME;
    if (!apiKey || !baseId || !tableName) throw new Error('Missing configuration');
    const result = await exportTasks({base: createBase(apiKey, baseId), tasks, projectId, tableName});
    process.stdout.write(JSON.stringify(result));
  } catch {
    // Never forward SDK messages, URLs, environment, or credentials.
    process.stdout.write(JSON.stringify({error: 'Airtable export could not start.'}));
    process.exitCode = 1;
  }
}
