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

// TODO: remove dashes from comments causing encoding issues

(function() {
    'use strict';

    let tracklist = []

    const table = document.querySelector(".tracklist_ZdQ0I")
    const rows = table.querySelectorAll("tr")

    for (const row of rows){
        let song = {}

        const td = row.querySelector('td.artist_VsG56');
        const artist = removeDashes(td);

        const trackPos = findDeepestChild(row.querySelector(".trackPos_n8vad")).innerText;
        const duration = findDeepestChild(row.querySelector(".duration_GhhxK")).innerText;

        const fullTitle = row.querySelector("td.trackTitle_loyWF");
        const title = fullTitle.querySelector("span.trackTitle_loyWF").innerText;
        const comments = fullTitle.children[1].querySelector(".css-144m4pk").innerText;
        
        song.title = title;
        song.artist = artist;
        song.trackPos = trackPos;
        song.duration = duration;
        song.comments = comments;

        tracklist.push(song);
    }

    const blob = new Blob([JSON.stringify(tracklist)], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "tracklist.json"; // File name
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url); // Clean up


})();

function removeDashes(td){
    const container = td.querySelector('span') || td;

    const clone = container.cloneNode(true);
    clone.querySelectorAll('.dash_vWaes').forEach(n => n.remove());

    const text = clone.textContent
    .replace(/\u00A0/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

    return text;
}


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