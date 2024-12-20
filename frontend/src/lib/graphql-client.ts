import config from '../config';

export class GraphQLError extends Error {
    constructor(public errors: any[]) {
        super(errors[0].message);
        this.name = 'GraphQLError';
    }
}

export async function graphqlRequest<T = any>(
    query: string,
    variables?: Record<string, any>
): Promise<T> {
    const response = await fetch(`${config.apiUrl}/graphql`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query,
            variables,
        }),
    });

    const result = await response.json();

    if (result.errors) {
        throw new GraphQLError(result.errors);
    }

    return result.data;
}