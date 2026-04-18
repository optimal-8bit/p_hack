import PropTypes from 'prop-types'

function escapeHtml(text) {
  return text
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;')
}

function inlineMarkdown(text) {
  let output = escapeHtml(text)
  output = output.replace(/`([^`]+)`/g, '<code>$1</code>')
  output = output.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
  output = output.replace(/\*([^*]+)\*/g, '<em>$1</em>')
  output = output.replace(
    /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,
    '<a href="$2" target="_blank" rel="noreferrer">$1</a>',
  )
  return output
}

function markdownToHtml(markdownText) {
  const lines = markdownText.split('\n')
  const blocks = []
  let inCodeBlock = false
  let codeBuffer = []
  let listType = null

  const closeList = () => {
    if (!listType) return
    blocks.push(`</${listType}>`)
    listType = null
  }

  for (const rawLine of lines) {
    const line = rawLine.trimEnd()

    if (line.startsWith('```')) {
      if (inCodeBlock) {
        blocks.push(`<pre><code>${escapeHtml(codeBuffer.join('\n'))}</code></pre>`)
        codeBuffer = []
        inCodeBlock = false
      } else {
        closeList()
        inCodeBlock = true
      }
      continue
    }

    if (inCodeBlock) {
      codeBuffer.push(rawLine)
      continue
    }

    if (!line) {
      closeList()
      continue
    }

    const headingMatch = line.match(/^(#{1,6})\s+(.*)$/)
    if (headingMatch) {
      closeList()
      const level = headingMatch[1].length
      blocks.push(`<h${level}>${inlineMarkdown(headingMatch[2])}</h${level}>`)
      continue
    }

    const unorderedMatch = line.match(/^[-*]\s+(.*)$/)
    if (unorderedMatch) {
      if (listType !== 'ul') {
        closeList()
        listType = 'ul'
        blocks.push('<ul>')
      }
      blocks.push(`<li>${inlineMarkdown(unorderedMatch[1])}</li>`)
      continue
    }

    const orderedMatch = line.match(/^\d+\.\s+(.*)$/)
    if (orderedMatch) {
      if (listType !== 'ol') {
        closeList()
        listType = 'ol'
        blocks.push('<ol>')
      }
      blocks.push(`<li>${inlineMarkdown(orderedMatch[1])}</li>`)
      continue
    }

    closeList()
    blocks.push(`<p>${inlineMarkdown(line)}</p>`)
  }

  if (inCodeBlock) {
    blocks.push(`<pre><code>${escapeHtml(codeBuffer.join('\n'))}</code></pre>`)
  }
  closeList()

  return blocks.join('')
}

export function MarkdownView({ content, isUser }) {
  return (
    <div
      className={`markdown-view ${isUser ? 'markdown-user' : 'markdown-assistant'}`}
      dangerouslySetInnerHTML={{ __html: markdownToHtml(content || '...') }}
    />
  )
}

MarkdownView.propTypes = {
  content: PropTypes.string,
  isUser: PropTypes.bool,
}
