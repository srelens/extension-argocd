import {test} from 'node:test';
import assert from 'node:assert/strict';
import {generateKeyPairSync,verify} from 'node:crypto';
import {mkdtempSync,mkdirSync,copyFileSync,writeFileSync,readFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
test('release signing requires the matching key and signs exact bytes',()=>{
 const dir=mkdtempSync(join(tmpdir(),'app-sign-test-'));
 try {
  mkdirSync(join(dir,'scripts'));mkdirSync(join(dir,'dist'));
  copyFileSync(new URL('../scripts/sign.mjs',import.meta.url),join(dir,'scripts/sign.mjs'));
  const {privateKey,publicKey}=generateKeyPairSync('ed25519');
  writeFileSync(join(dir,'signing-public.pem'),publicKey.export({type:'spki',format:'pem'}));
  const raw=Buffer.from('{"id":"test.app"}\n');
  writeFileSync(join(dir,'dist/manifest.json'),raw);
  const run=key=>spawnSync(process.execPath,['scripts/sign.mjs'],{cwd:dir,env:{...process.env,APP_SIGNING_PRIVATE_KEY:key},encoding:'utf8'});
  assert.notEqual(run('').status,0);
  assert.notEqual(run(generateKeyPairSync('ed25519').privateKey.export({type:'pkcs8',format:'pem'})).status,0);
  assert.equal(run(privateKey.export({type:'pkcs8',format:'pem'})).status,0);
  const sig=readFileSync(join(dir,'dist/manifest.json.sig'));
  assert.equal(sig.length,64);assert.equal(verify(null,raw,publicKey,sig),true);
  assert.equal(verify(null,Buffer.concat([raw,Buffer.from(' ')]),publicKey,sig),false);
 } finally {rmSync(dir,{recursive:true,force:true});}
});
