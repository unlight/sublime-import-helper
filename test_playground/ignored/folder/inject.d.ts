/**
 * Inject a dependency
 * @param token The DI-token
 * @param factory Factory function that returns the dependency
 * @returns The dependency or a mock object if the dependency was mocked using mock()
 */
export declare const inject: <T>(token: string, factory: () => T) => T;
export declare const injector: {
    provide: (token: string, value: () => any) => void;
    mock: (token: string, value: () => any) => void;
    clear: () => void;
};
