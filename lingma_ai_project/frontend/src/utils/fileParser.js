import * as pdfjsLib from 'pdfjs-dist'

// 设置worker
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js'

/**
 * 从PDF文件提取文本
 */
export async function parsePDF(file) {
  try {
    const arrayBuffer = await file.arrayBuffer()
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise
    let text = ''
    
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i)
      const content = await page.getTextContent()
      text += content.items.map(item => item.str).join(' ') + '\n'
    }
    
    return text
  } catch (error) {
    console.error('PDF解析错误:', error)
    throw new Error(`PDF解析失败: ${error.message}`)
  }
}

/**
 * 从文本文件提取内容
 */
export async function parseTextFile(file) {
  try {
    return await file.text()
  } catch (error) {
    console.error('文本文件解析错误:', error)
    throw new Error(`文本文件解析失败: ${error.message}`)
  }
}

/**
 * 根据文件类型解析文件
 */
export async function parseFile(file) {
  if (!file) {
    throw new Error('文件不能为空')
  }
  
  if (file.type === 'application/pdf' || file.name.endsWith('.pdf')) {
    return await parsePDF(file)
  } else if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
    return await parseTextFile(file)
  } else {
    throw new Error('不支持的文件类型，仅支持PDF和TXT文件')
  }
}
