// ==UserScript==
// @name         Discogs Tracklist Downloader
// @namespace    http://tampermonkey.net/
// @version      2025-08-31
// @description  downloads tracklist as json
// @author       abshta9000
// @match        https://www.discogs.com/release/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=discogs.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    let tracklist = []

    const table = document.querySelector(".tracklist_ZdQ0I")
    const rows = table.querySelectorAll("tr")

    for (const row of rows){
        let song = {}

        const artist = row.querySelector(".artist_VsG56").innerText;
        const trackPos = findDeepestChild(row.querySelector(".trackPos_n8vad")).innerText;
        const duration = findDeepestChild(row.querySelector(".duration_GhhxK")).innerText;

        const fullTitle = row.querySelector("td.trackTitle_loyWF");
        const title = fullTitle.querySelector("span.trackTitle_loyWF").innerText;
        const comments = fullTitle.children[1].querySelector(".css-144m4pk").innerText;

        const cd = trackPos.split("-")[0];
        const songNum = trackPos.split("-")[1];

        song.title = title;
        song.artist = artist;
        song.trackPos = trackPos;
        song.duration = duration;
        song.comments = comments;

        tracklist.push(song);
    }

    const blob = new Blob([JSON.stringify(tracklist)], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "tracklist.json"; // File name
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url); // Clean up


})();

function findDeepestChild(root) {
  let maxDepth = -1;
  let deepestNode = null;

  function traverse(node, depth) {
    if (!node) return;

    // Check if it's an element node
    if (node.nodeType === Node.ELEMENT_NODE) {
      if (depth > maxDepth) {
        maxDepth = depth;
        deepestNode = node;
      }

      // Recursively check child nodes
      for (let child of node.children) {
        traverse(child, depth + 1);
      }
    }
  }

  traverse(root, 0);
  return deepestNode;
}