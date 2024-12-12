import { useEffect, useRef, useState } from 'react';
import { Stream } from '@routes/Session/Session';
import { Markdown } from '@components/markdown/markdown';

interface ChatOutputProps {
	session: Stream[];
	stream: Stream;
}

export const ChatOutput = ({ session, stream }: ChatOutputProps) => {
	const [useAutoScroll, setUseAutoScroll] = useState(true);
	const scrollableArea = useRef<HTMLDivElement | null>(null);

	useEffect(() => {
		function handleScroll() {
			if (scrollableArea && scrollableArea.current) {
				const { scrollTop, scrollHeight, clientHeight } = scrollableArea.current;
				const distanceFromBottom = scrollHeight - (scrollTop + clientHeight);
				setUseAutoScroll(distanceFromBottom <= 20); // greater than 150px from bottom
			}
		}

		const scrollArea = scrollableArea.current;
		if (scrollArea) {
			scrollArea.addEventListener('scroll', handleScroll);
			return () => scrollArea.removeEventListener('scroll', handleScroll);
		}
	}, []);

	useEffect(() => {
		if (scrollableArea && scrollableArea.current && useAutoScroll) {
			// scroll to bottom of pane
			scrollableArea.current.scrollTop = scrollableArea.current.scrollHeight;
		}
	}, [session, stream, useAutoScroll]);

	return (
		<div className="flex flex-grow flex-col overflow-y-auto sm:px-2" ref={scrollableArea}>
			<ul className="flex flex-col gap-4">
				{session.map(({ human, ai }, i) => (
					<Conversation key={i} input={human as string} response={ai as string} />
				))}
				{stream.human && stream.ai && <Conversation input={stream.human} response={stream.ai} />}
			</ul>
		</div>
	);
};

export default ChatOutput;

function Conversation({ input, response }: { input: string; response: string }) {
	return (
		<>
			<li className="flex justify-end pl-20">
				<div className="rounded-[5px] border bg-gray-200 p-2 dark:border-neutral-700">
					<p className="text-sm font-semibold text-gray-400 text-gray-800">{input}</p>
				</div>
			</li>
			<li className="pr-20">
				<div className="rounded-[5px] border bg-white p-2 dark:border-none dark:bg-neutral-800 dark:text-gray-200">
					<Markdown markdown={response} />
				</div>
			</li>
		</>
	);
}
