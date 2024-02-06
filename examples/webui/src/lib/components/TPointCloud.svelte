<script lang="ts">
	import { Canvas, T } from '@threlte/core';

	export let vertices : Float32Array  |null = null;
	export let colors: Float32Array  |null = null;
    export let pointSize: number = 0.01;
	
</script>

<T.Points>
    <T.BufferGeometry>
        {#if vertices !=null}
            <T.BufferAttribute
                args={[vertices, 3]}
                attach={(parent, self) => {
                    parent.setAttribute('position', self);
                    return () => {
                    };
                }}
            />
        {/if}

        {#if colors !=null}
            <T.BufferAttribute
                args={[colors, 3]}
                attach={(parent, self) => {
                    parent.setAttribute('color', self);
                    return () => {
                    };
                }}
            />
        {/if}
    </T.BufferGeometry>
    
    {#if colors !=null}
        <T.PointsMaterial size={pointSize} vertexColors={true} />
    {:else}
        <T.PointsMaterial size={pointSize} color="red"/>
    {/if}
    <!-- <T.MeshBasicMaterial color="hotpink" /> -->
</T.Points>