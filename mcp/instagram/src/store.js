import fs from 'node:fs'
import path from 'node:path'

// Arquivo JSON com escrita atômica. Suficiente para um único processo com poucos milhares de registros.
export class JsonFile {
  constructor(file, fallback) {
    this.file = file
    this.fallback = fallback
  }

  read() {
    try {
      return JSON.parse(fs.readFileSync(this.file, 'utf8'))
    } catch (e) {
      if (e.code === 'ENOENT') return structuredClone(this.fallback)
      throw e
    }
  }

  write(data) {
    fs.mkdirSync(path.dirname(this.file), { recursive: true })
    const tmp = `${this.file}.${process.pid}.tmp`
    fs.writeFileSync(tmp, JSON.stringify(data, null, 2))
    fs.renameSync(tmp, this.file)
  }
}
