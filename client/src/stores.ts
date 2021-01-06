import { writable } from 'svelte/store';

export const players_store = writable([]);
export const CLIENT_STATE_STORE = writable("");
export const SERVER_STATE_STORE = writable("");