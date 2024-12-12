import { useState } from 'react';
import { Button, IconButton, TextArea, Tooltip } from '@centml/ui';

interface ChatControlsProps {
	isLoading?: boolean;
	isStreaming?: boolean;
	handleSubmit: (input: string) => void;
	handleStop?: () => void;
}

const PRESSED_KEYS: Record<string, boolean> = {};

const ChatControls = ({ handleSubmit, handleStop, isLoading, isStreaming }: ChatControlsProps) => {
	const [query, setQuery] = useState('');

	return (
		<div className="mt-2 flex flex-col gap-1 sm:px-2">
			<form
				className="flex flex-grow flex-row gap-2"
				onSubmit={(e) => {
					e.preventDefault();
					handleSubmit(query);
					setQuery('');
				}}
			>
				<div className="flex-grow">
					<TextArea
						autosize
						isRequired
						label="query"
						labelHidden
						maxLength={1500}
						maxRows={2}
						onKeyDown={(e) => {
							const { key } = e;
							PRESSED_KEYS[key] = true;

							if (key === 'Enter' && !PRESSED_KEYS['Shift']) {
								e.preventDefault();
								if (!query.trim()) return;

								handleSubmit(query);
								setQuery('');
							}
						}}
						onKeyUp={({ key }) => (PRESSED_KEYS[key] = false)}
						onChange={(value) => setQuery(value)}
						placeholder="Enter a message or question"
						value={query}
					/>
				</div>

				<div className="flex items-center gap-3">
					{(isLoading || isStreaming) && (
						<Tooltip tip="Stop request">
							<IconButton icon="stop-circle" squared label="stop request" onPress={handleStop} />
						</Tooltip>
					)}
					<Button loading={isLoading || isStreaming} type="submit" variant="primary">
						Submit
					</Button>
				</div>
			</form>
		</div>
	);
};

export default ChatControls;
