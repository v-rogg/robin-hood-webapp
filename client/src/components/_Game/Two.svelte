<script lang="ts">
    import {onMount} from "svelte";
    import Two from "two.js";

    export let sensor_darts = [];

    let two = new Two({
        autostart: true,
        height: 300,
        width: 300,
    })

    let loaded = false;

    const scale = two.width/451;

    let dart = Array.from(Array(3), () => new Array(2));

    onMount(() =>  {
        two.appendTo(document.getElementById('two'));
        loaded = true;
    })

    function update_darts(sensor_darts) {
        for (let i = 0; i < sensor_darts.length; i++) {
            if (dart[i][0]) {
                dart[i][0].remove()
            }
            if (dart[i][1]) {
                dart[i][1].remove()
            }
            if (dart[i][2]) {
                dart[i][2].remove()
            }

            const x = sensor_darts[i][0] * scale
            const y = -sensor_darts[i][1] * scale

            let d = two.makeCircle(x + (two.width / 2), y + (two.height / 2), 10)
            d.noStroke()
            d.opacity = .35;
            let c = two.makeCircle(x + (two.width / 2), y + (two.height / 2), 4)
            c.linewidth = 2;
            d.fill = '#18A0FB';
            c.fill = '#FFFFFF';

            let t;

            switch(i) {
                case 0:
                    t = two.makeText('1', x + (two.width / 2), y + (two.height / 2) - 17, 'normal')
                    // c.fill = '#00FFFF';
                    // d.fill = '#00FFFF';
                    break;
                case 1:
                    t = two.makeText('2', x + (two.width / 2), y + (two.height / 2) - 17, 'normal')
                    // c.fill = '#FF00FF';
                    // d.fill = '#FF00FF';
                    break;
                case 2:
                    t = two.makeText('3', x + (two.width / 2), y + (two.height / 2) - 17, 'normal')

                    // c.fill = '#FFFF00';
                    // d.fill = '#FFFF00';
                    break;
            }

            t.fill = '#FFFFFF';
            t.family = 'Rubik';
            t.size = 20;
            t.weight = 700;
            t.linewidth = 1;
            t.stroke = '#000000';

            dart[i][0] = c
            dart[i][1] = d
            dart[i][2] = t
            // setTimeout(() => {
            //     c.remove()
            //     d.remove()
            // }, 500)
        }

    }

    $: update_darts(sensor_darts);

</script>

<style lang="sass">
    #two
        position: absolute
        width: 300px
        margin: 0 auto
        left: 0
        right: 0
</style>

<div id="two"></div>