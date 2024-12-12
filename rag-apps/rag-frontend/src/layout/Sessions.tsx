import { useState } from 'react';
import { Link, useLocation, useNavigate, useSubmit } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Alert, ConfirmationModal, Icon, IconButton, Skeleton, toast, Tooltip } from '@centml/ui';
import { getSessions, sessionKeys } from '@api/sessions/sessions';
import { SessionData } from '@api/sessions/types';
import { ROUTES } from '@routes/routes.paths';

interface ChatSessionsProps {
	isCollapsed?: boolean;
	isMobile?: boolean;
}

const ChatSessions = ({ isCollapsed, isMobile }: ChatSessionsProps) => {
	const [showConfirmation, setShowConfirmation] = useState(false);
	const [selectedId, setSelectedId] = useState<null | string>(null);

	const { data, isLoading, error } = useQuery<SessionData[]>({ queryKey: sessionKeys.listSessions(), queryFn: getSessions });

	const navigate = useNavigate();
	const location = useLocation();
	const submit = useSubmit();

	if (error) console.error(error);

	return (
		<>
			<div className="mb-1 flex flex-grow flex-col gap-2 overflow-y-auto">
				<ul className="flex flex-col px-2">
					{isLoading && (
						<Skeleton>
							<Skeleton.Text />
							<Skeleton.Text />
							<Skeleton.Text />
						</Skeleton>
					)}

					{error && (
						<>
							<div className={isCollapsed ? 'hidden' : 'block'}>
								<Alert variant="error" showIcon>
									Could not retrieve chat history
								</Alert>
							</div>
							<div className={isCollapsed ? 'block flex justify-center' : 'hidden'}>
								<Tooltip tip="Could not get chat history">
									<IconButton
										className="h-8 w-8 !text-error-500"
										icon="exclamation-circle"
										label="could not get chat history"
										onPress={() => toast('Could not get chat history', { type: 'error' })}
										squared
									/>
								</Tooltip>
							</div>
						</>
					)}

					{data?.map(({ id, content }, i) => {
						const isSelected = location.pathname.includes(id);

						if (isCollapsed) {
							return (
								<li className="my-1 flex justify-center" key={i}>
									<Tooltip tip={content}>
										<IconButton
											className="h-8 w-8 text-white"
											icon="chat-bubble-left-right"
											label={`view session ${i}`}
											onPress={() => navigate(id)}
											squared
										/>
									</Tooltip>
								</li>
							);
						}

						return (
							<li
								key={i}
								className={`group flex items-center justify-between gap-1 rounded-md opacity-80 transition-colors hover:opacity-100 ${isSelected && 'bg-gray-100 !text-black opacity-100'} ${isMobile ? 'text-black dark:text-white' : 'text-white'}`}
							>
								<Link className="flex-grow truncate py-2 pl-4 text-left text-sm" to={id}>
									{content}
								</Link>

								<IconButton
									className={`opacity-0 group-hover:opacity-100 ${isSelected ? 'group-hover:text-black' : 'group-hover:text-white'} ${isMobile ? 'text:black opacity-100 dark:text-white' : ''}`}
									label="delete session"
									icon="trash"
									squared
									onPress={() => {
										setSelectedId(id);
										setShowConfirmation(true);
									}}
								/>
							</li>
						);
					})}
					{isCollapsed ? (
						<li className="my-1 flex justify-center">
							<Tooltip tip="New session" delay={1000}>
								<IconButton className="h-8 w-8 text-white" icon="plus" label="new session" onPress={() => navigate(ROUTES.DASHBOARD)} squared />
							</Tooltip>
						</li>
					) : (
						<li
							className={`flex items-center justify-between gap-1 rounded-md opacity-80 transition-colors hover:opacity-100 ${isMobile ? 'text-black dark:text-white' : 'text-white'}`}
						>
							<Link className="mt-2 flex flex-grow items-center gap-1 py-2 pl-4 text-left text-sm sm:justify-between" to={ROUTES.DASHBOARD}>
								New Session
								<Icon icon="plus" aria-hidden />
							</Link>
						</li>
					)}
				</ul>
			</div>

			<ConfirmationModal
				title="Delete session"
				variant="destructive"
				isOpen={!!showConfirmation}
				onOpenChange={() => setShowConfirmation(false)}
				onConfirm={() => {
					if (!selectedId) return;

					const formData = new FormData();
					formData.append('id', selectedId);
					submit(formData, { method: 'POST' });
					setShowConfirmation(false);
				}}
			>
				<p>Are you sure you want to delete this chat session? This action is permanent and cannot be undone.</p>
			</ConfirmationModal>
		</>
	);
};

export default ChatSessions;
