import test from 'node:test';
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import Airtable from 'airtable';
import {exportTasks} from './exporter.mjs';

function fakeAirtable() {
  const rows = new Map();
  const calls = [];
  return {rows, calls, async makeRequest(options) {
    calls.push(options);
    if (options.method !== 'PATCH') {
      const start = Number(options.qs.offset || 0);
      const records = [...rows.values()].slice(start, start + 100);
      return {body: {records, ...(start + 100 < rows.size ? {offset: String(start + 100)} : {})}};
    }
    assert.deepEqual(options.body.performUpsert, {fieldsToMergeOn: ['Task ID']});
    const createdRecords = [], updatedRecords = [], records = [];
    for (const record of options.body.records) {
      const id = record.fields['Task ID'];
      const previous = rows.get(id);
      const row = {id: previous?.id || `rec${rows.size}`, fields: record.fields};
      (previous ? updatedRecords : createdRecords).push(row.id);
      rows.set(id, row);
      records.push(row);
    }
    return {body: {records, createdRecords, updatedRecords}};
  }};
}

const task = (id) => ({id, title: `Task ${id}`, description: 'Details', status: 'todo', assignee: '', position: 0});
const options = (base, tasks) => ({base, tasks, projectId: 'project-1', tableName: 'Tasks', sleep: async () => {}});

test('repeated exports upsert by stable task ID without duplicate records', async () => {
  const base = fakeAirtable();
  const tasks = [task('one'), task('two')];
  const first = await exportTasks(options(base, tasks));
  const second = await exportTasks(options(base, tasks));
  assert.deepEqual([first.created, first.updated, first.failed], [2, 0, 0]);
  assert.deepEqual([second.created, second.updated, second.failed], [0, 2, 0]);
  assert.equal(base.rows.size, 2);
});

const failure = (statusCode, error = 'SERVICE_UNAVAILABLE') => Object.assign(new Error('never expose upstream details'), {statusCode, error});

test('retries transient failures with bounded exponential backoff', async () => {
  const base = fakeAirtable(), original = base.makeRequest.bind(base), delays = [];
  let attempts = 0;
  base.makeRequest = async o => {
    if (o.method === 'PATCH' && ++attempts < 3) throw failure(503);
    return original(o);
  };
  const result = await exportTasks({...options(base, [task('one')]), sleep: async ms => delays.push(ms)});
  assert.equal(result.created, 1);
  assert.equal(attempts, 3);
  assert.ok(delays.includes(500) && delays.includes(1000));
});

test('permanent authentication failures are not retried or exposed', async () => {
  let calls = 0;
  const base = {async makeRequest() {calls++; throw failure(401);}};
  const result = await exportTasks(options(base, [task('one'), task('two')]));
  assert.equal(calls, 1);
  assert.equal(result.failed, 2);
  assert.ok(!JSON.stringify(result).includes('upstream details'));
});

test('isolates a rejected record and continues with the rest of every batch', async () => {
  const base = fakeAirtable(), original = base.makeRequest.bind(base);
  let badSingletons = 0;
  const delays = [];
  base.makeRequest = async o => {
    if (o.method === 'PATCH' && o.body.records.some(r => r.fields['Task ID'] === 'bad')) {
      if(o.body.records.length === 1) badSingletons++;
      throw failure(422, 'INVALID_VALUE_FOR_COLUMN');
    }
    return original(o);
  };
  const tasks = [task('bad'), ...Array.from({length: 11}, (_, i) => task(String(i)))];
  const result = await exportTasks({...options(base, tasks), sleep: async ms => delays.push(ms)});
  assert.deepEqual([result.created, result.updated, result.failed], [11, 0, 1]);
  assert.equal(result.failures[0].taskId, 'bad');
  assert.equal(badSingletons, 1);
  assert.ok(delays.every(ms => ms === 250));
});

test('exports 1000 tasks in ten-record batches and follows all read pages', async () => {
  const base = fakeAirtable();
  const tasks = Array.from({length: 1000}, (_, i) => task(String(i)));
  for (const t of tasks) base.rows.set(t.id, {id: `rec${t.id}`, fields: {'Task ID': t.id}});
  const result = await exportTasks(options(base, tasks));
  const reads = base.calls.filter(c => c.method !== 'PATCH');
  const writes = base.calls.filter(c => c.method === 'PATCH');
  assert.deepEqual([result.created, result.updated, result.failed], [0, 1000, 0]);
  assert.equal(reads.length, 10);
  assert.equal(reads.at(-1).qs.offset, '900');
  assert.ok(reads.every(c => c.qs.pageSize === 100 && c.qs.filterByFormula === '{Project ID}="project-1"'));
  assert.equal(writes.length, 100);
  assert.ok(writes.every(c => c.body.records.length === 10));
});

test('an ambiguous network failure after a committed write cannot create duplicates', async () => {
  const base = fakeAirtable(), original = base.makeRequest.bind(base);
  let attempts = 0;
  base.makeRequest = async o => {
    const response = await original(o);
    if (o.method === 'PATCH' && ++attempts === 1) throw failure(null, 'CONNECTION_ERROR');
    return response;
  };
  const result = await exportTasks(options(base, [task('one')]));
  assert.deepEqual([result.created, result.updated, result.failed], [0, 1, 0]);
  assert.equal(attempts, 2);
  assert.equal(base.rows.size, 1);
});

test('rate limits back off for 30 then 60 seconds and stop after three attempts', async () => {
  const base = fakeAirtable(), original = base.makeRequest.bind(base), delays = [];
  let attempts = 0;
  base.makeRequest = async o => {
    if (o.method === 'PATCH') { attempts++; throw failure(429, 'TOO_MANY_REQUESTS'); }
    return original(o);
  };
  const result = await exportTasks({...options(base, [task('one')]), sleep: async ms => delays.push(ms)});
  assert.equal(attempts, 3);
  assert.equal(result.failed, 1);
  assert.deepEqual(delays.filter(ms => ms !== 250), [30000, 60000]);
});

test('a permanent monthly billing limit is never retried', async () => {
  let calls = 0;
  const base = {async makeRequest() { calls++; throw failure(429, 'PUBLIC_API_BILLING_LIMIT_EXCEEDED'); }};
  const result = await exportTasks(options(base, [task('one')]));
  assert.equal(calls, 1);
  assert.equal(result.failed, 1);
});

test('exhausting one batch of transient errors still exports later batches', async () => {
  const base = fakeAirtable(), original = base.makeRequest.bind(base);
  let failedAttempts = 0;
  base.makeRequest = async o => {
    if (o.method === 'PATCH' && o.body.records.some(r => r.fields['Task ID'] === '0')) {
      failedAttempts++; throw failure(503);
    }
    return original(o);
  };
  const result = await exportTasks(options(base, Array.from({length: 11}, (_, i) => task(String(i)))));
  assert.deepEqual([result.created, result.updated, result.failed], [1, 0, 10]);
  assert.equal(failedAttempts, 3);
  assert.ok(base.rows.has('10'));
});

test('the total duration budget returns partial results instead of retrying forever', async () => {
  const base = fakeAirtable();
  let elapsed = 0;
  const result = await exportTasks({...options(base, Array.from({length: 11}, (_, i) => task(String(i)))),
    now: () => elapsed, sleep: async ms => { elapsed += ms; }, maxDurationMs: 700});
  assert.deepEqual([result.created, result.updated, result.failed], [10, 0, 1]);
  assert.match(result.failures[0].error, /time limit/);
});

test('existing duplicate Task IDs fail only that task without adding another copy', async () => {
  const base = fakeAirtable(), original = base.makeRequest.bind(base);
  base.makeRequest = async o => o.method === 'PATCH' ? original(o) : {body: {records: [
    {fields: {'Task ID': 'duplicate'}}, {fields: {'Task ID': 'duplicate'}},
  ]}};
  const result = await exportTasks(options(base, [task('duplicate'), task('good')]));
  assert.deepEqual([result.created, result.updated, result.failed], [1, 0, 1]);
  assert.equal(result.failures[0].taskId, 'duplicate');
  assert.ok(!base.rows.has('duplicate'));
});

test('official Airtable SDK sends the upsert payload and does not secretly retry 429s', async t => {
  const received = [];
  let rateLimited = false;
  const server = createServer(async (req, res) => {
    let raw = '';
    for await (const chunk of req) raw += chunk;
    received.push({method: req.method, url: req.url, body: raw && JSON.parse(raw)});
    res.setHeader('Content-Type', 'application/json');
    if (rateLimited) {
      res.writeHead(429);
      res.end(JSON.stringify({error: {type: 'TOO_MANY_REQUESTS', message: 'limited'}}));
    } else if (req.method === 'PATCH') {
      res.end(JSON.stringify({records: [{id: 'rec1'}], createdRecords: ['rec1'], updatedRecords: []}));
    } else res.end(JSON.stringify({records: []}));
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => server.close(resolve)));
  const base = new Airtable({apiKey: 'test-only', endpointUrl: `http://127.0.0.1:${server.address().port}`,
    noRetryIfRateLimited: true, requestTimeout: 1000}).base('appTestOnly');
  const result = await exportTasks(options(base, [task('one')]));
  assert.equal(result.created, 1);
  assert.match(received[0].url, /pageSize=100/);
  assert.equal(new URL(received[1].url, 'http://localhost').pathname, '/v0/appTestOnly/Tasks');
  assert.deepEqual(received[1].body.performUpsert, {fieldsToMergeOn: ['Task ID']});
  assert.equal(received[1].body.records[0].fields['Task Description'], 'Details');
  rateLimited = true;
  const limited = await exportTasks(options(base, [task('one')]));
  assert.equal(limited.failed, 1);
  assert.equal(received.length, 5); // two success calls plus three bounded 429 calls
});
