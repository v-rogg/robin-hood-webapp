<script lang="ts">
    import {CLIENT_STATE_STORE, SERVER_STATE_STORE} from "../../stores";

    let CLIENT_STATE, SERVER_STATE;
    CLIENT_STATE_STORE.subscribe(value => CLIENT_STATE = value);
    SERVER_STATE_STORE.subscribe(value => SERVER_STATE = value);
</script>

<style lang="sass">
    .states
        position: fixed
        bottom: 3rem
        left: 3rem
        text-align: left

    span
        font-style: italic
</style>

<div class="states">
    <div>
        Client State: <span>{CLIENT_STATE}</span>
    </div>
    <div>
        Server State: <span>{SERVER_STATE}</span>
    </div>
</div>