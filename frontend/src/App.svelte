<script>
  import Router from "svelte-spa-router";

  import Home from "./routes/Home.svelte";
  import Dashboard from "./routes/Dashboard.svelte";
  import Search from "./routes/Search.svelte";
  import Viewer from "./routes/DocViewer.svelte";

  const routes = {
    "/": Home,
    "/dashboard/:subpage?": Dashboard,
    "/search": Search,
    "/view": Viewer,
    "*": Home,
  };
</script>

<main>
  <Router {routes} />
</main>
