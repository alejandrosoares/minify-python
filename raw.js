import api from "./wp_api.js";
import request from "./request.js";
import showLoader from "./loader.js";
import { Card as CardPost } from "../components/home/cards.js";
import { Card as CardSearch } from "../components/search/cards.js";

function verifyIfH2Exists(postsContainer) {
   /*
    Remove h2 if it exists
    @param: div.posts
    */
   const h2 = postsContainer.querySelector("h2");

   if (h2) h2.remove();
}

export async function infiniteScroll() {
   window.addEventListener("scroll", async (e) => {
      let query = localStorage.getItem("query"),
         apiUrl,
         Component,
         { hash } = location;

      let { scrollTop, clientHeight, scrollHeight } = document.documentElement;

      if (scrollTop + clientHeight >= scrollHeight) {
         api.page++;

         if (hash === "") {
            // Home
            apiUrl = `${api.POSTS}&page=${api.page}`;
         } else if (hash.includes("#search")) {
            // Search
            apiUrl = `${api.SEARCH}${query}&page=${api.page}`;
         } else {
            return false;
         }

         showLoader(true);

         await request({
            url: apiUrl,
            cbSuccess: (posts) => {
               const postsContainer = document.querySelector("#main .posts");
               let html = "";

               if (hash === "") {
                  const fastMode = localStorage.getItem("fast-mode") || "false";

                  posts.forEach((post) => (html += CardPost(post, fastMode)));
               } else {
                  // If the request takes time and the section is changed,
                  // then postsContainer is null
                  if (postsContainer) verifyIfH2Exists(postsContainer);

                  posts.forEach((post) => (html += CardSearch(post)));
               }

               // If the request takes time and the section is changed,
               // then postsContainer is null
               if (postsContainer)
                  postsContainer.insertAdjacentHTML("beforeend", html);

               showLoader(false);
            },
         });
      }
   });
}
