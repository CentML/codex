import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { IconButton, Tooltip, useClipboard } from '@centml/ui';

interface MarkdownProps {
	isStream?: boolean;
	markdown: string;
}

export const Markdown = ({ isStream, markdown }: MarkdownProps) => {
	const [showCopied, setShowCopied] = useState<string | null>(null);
	const { copyToClipboard } = useClipboard();

	const handleCopy = (code: string) => {
		copyToClipboard(code);
		setShowCopied(code.slice(0, 10));

		setTimeout(() => setShowCopied(null), 1000);
	};

	return (
		<ReactMarkdown
			children={markdown}
			components={{
				p: ({ children, ...props }) => (
					<p className="my-4 first:mt-0 last:mb-0" {...props}>
						{children}
					</p>
				),
				code: ({ children, className, ...props }) => {
					const match = /language-(\w+)/.exec(className || '');
					const codeContent = String(children).replace(/\n$/, '');
					const isSingleLine = !codeContent.includes('\n');

					return isSingleLine ? (
						<code style={{ fontSize: '14px', padding: '2px 4px', borderRadius: '5px', backgroundColor: '#f3f4f6' }}>{children}</code>
					) : (
						<div className="relative">
							{/* @ts-ignore-next-line */}
							<SyntaxHighlighter
								PreTag="div"
								customStyle={{ fontSize: '14px', padding: '4px', borderRadius: '5px', display: isSingleLine ? 'inline' : 'block' }}
								language={match ? match[1] : 'python'}
								wrapLongLines
								{...props}
							>
								{codeContent}
							</SyntaxHighlighter>
							{!isStream && (
								<div className="absolute bottom-1 right-1 flex justify-end">
									<Tooltip tip="Copied" isOpen={showCopied === codeContent.slice(0, 10)}>
										<IconButton className="h-6 w-6" label="copy code" icon="document-duplicate" squared onPress={() => handleCopy(codeContent)} />
									</Tooltip>
								</div>
							)}
						</div>
					);
				}
			}}
		/>
	);
};
