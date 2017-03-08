let dependencies: {[id: string]: () => any} = {};

const provide = (token: string, value: () => any) => {
	dependencies[token] = value;
};

const clear = () => {
	dependencies = {};
};
/**
 * Inject a dependency
 * @param token The DI-token
 * @param factory Factory function that returns the dependency
 * @returns The dependency or a mock object if the dependency was mocked using mock()
 */
export const inject = <T>(token: string, factory: () => T): T  => {
	if (typeof dependencies[token] !== 'undefined') {
		return dependencies[token]();
	}
	return factory();
};

export const injector = {
	provide: provide,
	mock: provide,
	clear: clear,
};
