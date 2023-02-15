<script lang="ts">
  import axios from 'axios'
  import { onMount } from 'svelte'

  let cameraName = 'Cam 1'
  let url = 'rtsp://admin:admin@192.168.0.104:554/11'

  interface ICamera {
    name: string
    id: string
  }

  let cameras: ICamera[] = []

  const getCameras = async () => {
    try {
      const { data } = await axios.get('http://localhost:5000/cameras')

      console.log('data', data)
      cameras = data
    } catch (error) {
      console.log('error', error)
    }
  }

  const add = async () => {
    try {
      const { data } = await axios.post('http://localhost:5000/cameras', {
        cameraName,
        cameraURL: url,
      })

      getCameras()
      console.log('data', data)
    } catch (error) {
      console.log('error', error)
    }
  }

  onMount(() => {
    getCameras()
  })
</script>

<main>
  <div class="cameras">
    {#each cameras as camera}
      <div class="cameraBox">
        <h3>{camera.name}</h3>
        <img src={`http://localhost:5000/stream?camera-id=${camera.id}`} alt="stream" />
      </div>
    {/each}
  </div>

  <div class="addBox">
    <input type="text" bind:value={cameraName} placeholder="Camera Name" />
    <input type="text" bind:value={url} placeholder="Camera URL" />
    <button on:click={add}>Add</button>
  </div>
</main>

<style>
  main {
    display: flex;
    height: 100vh;
    background-color: #14181b;
  }

  .cameras {
    flex: 1;
    flex-grow: 1;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    padding: 1rem;
  }

  .cameraBox {
  }

  .cameraBox img {
    width: 100%;
  }

  .addBox {
    background-color: #222;
    height: 100%;
    padding: 2rem;
    display: flex;
    flex-direction: column;
  }
</style>
