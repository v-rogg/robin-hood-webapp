import { writable } from 'svelte/store';

export const PLAYERS_STORE = writable([]);
export const CLIENT_STATE_STORE = writable('');
export const SERVER_STATE_STORE = writable('');
export const GAMEMODE_STORE = writable('');
export const DARTS_STORE = writable([]);
