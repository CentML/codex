// session data is the list of ids and the first query submitted by the user for that session
export interface SessionData {
	id: string;
	content: string;
}

export interface JSONSession {
	type: 'human' | 'ai';
	data: {
		content: string;
		additional_kwargs: {
			[key: string]: unknown;
		};
		response_metadata: { [key: string]: unknown };
		type: 'human' | 'ai';
		name: unknown;
		id: unknown;
		example: unknown;
	};
}
