/**
 * Falha se algum arquivo versionado tiver cara de segredo.
 * Roda a partir de backend/: node scripts/check-segredo.mjs
 */
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const PADROES = [
  { nome: 'chave privada', re: /-----BEGIN [A-Z ]*PRIVATE KEY-----/ },
  { nome: 'chave AWS', re: /\bAKIA[0-9A-Z]{16}\b/ },
  { nome: 'URL de banco com senha', re: /\bpostgres(?:ql)?:\/\/[^:/\s]+:[^@\s]+@(?!host\b)/ },
  { nome: 'token do GitHub', re: /\bgh[opsu]_[A-Za-z0-9]{30,}\b/ },
  { nome: 'chave de API genérica', re: /\bsk-[A-Za-z0-9]{24,}\b/ },
];

const IGNORAR = new Set(['backend/scripts/check-segredo.mjs']);

const raiz = execFileSync('git', ['rev-parse', '--show-toplevel'], { encoding: 'utf8' }).trim();
const arquivos = execFileSync('git', ['ls-files'], { cwd: raiz, encoding: 'utf8' })
  .split('\n')
  .filter((arquivo) => arquivo && !IGNORAR.has(arquivo) && !/\.(png|jpe?g|ico|woff2?|zip|drawio)$/i.test(arquivo) && !arquivo.endsWith('package-lock.json'));

const achados = [];
for (const arquivo of arquivos) {
  let texto;
  try {
    texto = readFileSync(resolve(raiz, arquivo), 'utf8');
  } catch {
    continue;
  }
  texto.split('\n').forEach((linha, indice) => {
    for (const padrao of PADROES) {
      if (padrao.re.test(linha)) achados.push(`${arquivo}:${indice + 1} — ${padrao.nome}`);
    }
  });
}

if (achados.length > 0) {
  console.error('Possível segredo versionado. Rotacione e remova:');
  achados.forEach((achado) => console.error(`  ${achado}`));
  process.exit(1);
}
console.log(`check:segredo ok — ${arquivos.length} arquivos verificados.`);
