<script>
  import { Dropzone, Button } from "flowbite-svelte";

  let value = [];
  let form_data = new FormData();

  const dropHandle = (event) => {
    value = [];
    event.preventDefault();
    if (event.dataTransfer.items) {
      [...event.dataTransfer.items].forEach((item, i) => {
        if (item.kind === "file") {
          const file = item.getAsFile();
          if (!(file.name in value)) {
            value.push(file.name);
            value = value;
            form_data.append("file", file);
          }
        }
      });
    } else {
      [...event.dataTransfer.files].forEach((file, i) => {
        value = file.name;
      });
    }
  };

  const handleChange = (event) => {
    const files = event.target.files;
    console.log(files);
    if (files.length > 0) {
      [...files].forEach((file, i) => {
        if (!(file.name in value)) {
          value.push(file.name);
          value = value;
          form_data.append("file", file);
        }
      });
    }
  };

  const showFiles = (files) => {
    if (files.length === 1) return files[0];
    let concat = "";
    files.map((file) => {
      concat += file;
      concat += ",";
      concat += " ";
    });

    if (concat.length > 40) concat = concat.slice(0, 40);
    concat += "...";
    return concat;
  };

  function handleSubmit(event) {
    const url = window.location.origin + "/api/docs/upload";
    const fetchOptions = {
      method: "post",
      body: form_data,
    };

    console.log(form_data.getAll("file"));

    fetch(url, fetchOptions);

    value = [];
    form_data = new FormData();
  }
</script>

<form>
  <Dropzone
    multiple
    id="dropzone"
    on:drop={dropHandle}
    on:dragover={(event) => {
      event.preventDefault();
    }}
    on:change={handleChange}
  >
    <svg
      aria-hidden="true"
      class="mb-3 w-10 h-10 text-gray-400"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
      ><path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
      /></svg
    >
    {#if value.length === 0}
      <p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
        <span class="font-semibold">Click to upload</span> or drag and drop
      </p>
      <p class="text-xs text-gray-500 dark:text-gray-400">
        SVG, PNG, JPG or GIF (MAX. 800x400px)
      </p>
    {:else}
      <p>{showFiles(value)}</p>
    {/if}
  </Dropzone>
  <Button on:click={handleSubmit} class="mt-5 pr-20 pl-20" color="primary"
    >Upload</Button
  >
</form>
