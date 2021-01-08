import App from './App.svelte';

const el = document.getElementById('app')

const app = new App({
	target: el,
});

export default app;