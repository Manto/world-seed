interface Config {
    apiUrl: string;
    graphqlEndpoint: string;
}

const config: Config = {
    apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    graphqlEndpoint: import.meta.env.VITE_GRAPHQL_ENDPOINT || '/graphql',
}

export const getGraphqlUrl = () => `${config.apiUrl}${config.graphqlEndpoint}`;

export default config;