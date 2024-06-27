<script>
  import { current_page } from "../stores";
  import { location } from "svelte-spa-router";
  import {
    Sidebar,
    SidebarGroup,
    SidebarItem,
    SidebarWrapper,
    SidebarBrand,
  } from "flowbite-svelte";
  import {
    ChartPieSolid,
    FolderOpenSolid,
    UploadSolid,
    UserSolid,
    ArrowRightToBracketOutline,
    EditOutline,
  } from "flowbite-svelte-icons";

  import Svg from "../assets/svelte.svg";

  const imports = {
    null: () => import("./dashboard_subpages/Main.svelte"),
    docs: () => import("./dashboard_subpages/Documents.svelte"),
    account: () => import("./dashboard_subpages/Account.svelte"),
    upload: () => import("./dashboard_subpages/Upload.svelte"),
  };

  let site = {
    name: "Jarwo Lookup",
    href: "/",
    img: Svg,
  };

  function lmao(event) {
    console.log(activeUrl);
  }

  $: activeUrl = "/#" + $location;

  export let params = {};

  $: console.log(activeUrl);
  let activeClass =
    "flex items-center p-2 text-base font-normal text-primary-900 bg-primary-200 dark:bg-primary-700 rounded-lg dark:text-white hover:bg-primary-100 dark:hover:bg-gray-700";
  let nonActiveClass =
    "flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-200 dark:hover:bg-gray-700";
  let iconClass =
    "w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white";
</script>

<div class="container mx-2">
  <!-- <img src={Svg} /> -->
  <div class="flex flex-row flex-wrap py-4">
    <aside class="w-full sm:w-1/3 md:w-1/4 px-2">
      <Sidebar {activeUrl} {activeClass} {nonActiveClass}>
        <nav class="divide-y divide-gray-200 dark:divide-gray-600">
          <SidebarWrapper>
            <SidebarBrand size="lg" {site} />
            <SidebarGroup>
              <SidebarItem label="Dashboard" href="/#/dashboard">
                <svelte:fragment slot="icon">
                  <ChartPieSolid class={iconClass} />
                </svelte:fragment>
              </SidebarItem>
              <SidebarItem label="Documents" href="/#/dashboard/docs">
                <svelte:fragment slot="icon">
                  <FolderOpenSolid class={iconClass} />
                </svelte:fragment>
              </SidebarItem>
              <SidebarItem label="Account" href="/#/dashboard/account">
                <svelte:fragment slot="icon">
                  <UserSolid class={iconClass} />
                </svelte:fragment>
              </SidebarItem>
              <SidebarItem label="Return" href="/">
                <svelte:fragment slot="icon">
                  <ArrowRightToBracketOutline class={iconClass} />
                </svelte:fragment>
              </SidebarItem>
            </SidebarGroup>
          </SidebarWrapper>
        </nav>
      </Sidebar>
    </aside>
    <main class="w-full sm:w-2/3 md:w-3/4 pt-1 pl-20">
      {#await imports[params.subpage]() then module}
        <svelte:component this={module.default} />
      {/await}
    </main>
  </div>
</div>
