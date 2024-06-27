<script>
  import { Search, Button, Card } from "flowbite-svelte";
  import { SearchOutline } from "flowbite-svelte-icons";
</script>

<div class="w-full p-4">
  <main class="w-full flex flex-col h-screen content-center justify-center">
    <div class="w-full sm:w-1/2 lg:w-1/3 m-auto">
      <Card size="md">
        <form class="flex gap-2">
          <Search size="md" color="dark" />
          <Button class="!p-2.5" color="dark">
            <SearchOutline class="w-6 h-6" />
          </Button>
        </form>
      </Card>
    </div>
  </main>
</div>
