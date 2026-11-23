// Render figures from the course website without shipping slide assets.
(() => {
  "use strict";

  const bootKey = Symbol.for("infinitepwn.courseFigures");
  if (window[bootKey]) {
    window[bootKey]();
    return;
  }

  const courseOrigin = "https://yuchen1024.github.io";
  const slidesPath = "/teaching/algorithm/lecture_slides/";
  const pdfJsPackage = "https://cdn.jsdelivr.net/npm/pdfjs-dist@6.5.438/";
  const buildPath = pdfJsPackage + "legacy/build/";
  const maxCanvasSide = 3072;
  const maxCanvasPixels = 3_000_000;
  const selector = "figure.course-figure[data-slide-src][data-slide-page][data-slide-crop]";
  const documents = new Map();
  const processedFigures = new WeakSet();
  let library;

  function loadLibrary() {
    if (!library) {
      library = import(buildPath + "pdf.min.mjs").then(pdfjs => {
        pdfjs.GlobalWorkerOptions.workerSrc = buildPath + "pdf.worker.min.mjs";
        return pdfjs;
      });
    }
    return library;
  }

  function getPage(url, number) {
    let entry = documents.get(url);
    if (!entry) {
      const loading = loadLibrary().then(pdfjs => pdfjs.getDocument({
        url,
        withCredentials: false,
        disableAutoFetch: true,
        disableStream: true,
        cMapUrl: pdfJsPackage + "cmaps/",
        standardFontDataUrl: pdfJsPackage + "standard_fonts/",
        wasmUrl: pdfJsPackage + "wasm/",
        iccUrl: pdfJsPackage + "iccs/"
      }).promise);
      entry = { loading, pages: new Map() };
      documents.set(url, entry);
    }
    if (!entry.pages.has(number)) {
      entry.pages.set(number, entry.loading.then(pdf => pdf.getPage(number)));
    }
    return entry.pages.get(number);
  }

  function readSource(figure) {
    const url = new URL(figure.dataset.slideSrc);
    const number = Number(figure.dataset.slidePage);
    if (url.origin !== courseOrigin || !url.pathname.startsWith(slidesPath) ||
        !url.pathname.endsWith(".pdf") || url.username || url.password || url.search ||
        !Number.isSafeInteger(number) || number < 1) {
      throw new Error("Invalid course slide source");
    }
    url.hash = "";
    return { url, number };
  }

  function readCrop(figure) {
    // Normalized coordinates in page display order: left, top, right, bottom.
    const parts = figure.dataset.slideCrop.split(",").map(part => part.trim());
    const crop = parts.map(Number);
    if (parts.length !== 4 || parts.some(part => !part) ||
        crop.some(edge => !Number.isFinite(edge) || edge < 0 || edge > 1) ||
        crop[0] >= crop[2] || crop[1] >= crop[3]) {
      throw new Error("Invalid course slide crop");
    }
    return crop;
  }

  function addNativePreview(figure, source) {
    const details = document.createElement("details");
    const summary = document.createElement("summary");
    details.className = "course-figure-fallback";
    summary.textContent = "在本页打开课件 PDF";
    details.append(summary);
    figure.insertBefore(details, figure.querySelector("figcaption"));

    details.addEventListener("toggle", function previewOnOpen() {
      if (!details.open) return;
      const frame = document.createElement("iframe");
      const target = new URL(source.url);
      target.hash = `page=${source.number}&view=FitH`;
      frame.title = `课程课件第 ${source.number} 页`;
      frame.referrerPolicy = "no-referrer";
      frame.height = "400";
      frame.style.cssText = "display:block;width:100%;height:min(70vh,36rem);border:0;";
      frame.src = target.href;
      details.append(frame);
      details.removeEventListener("toggle", previewOnOpen);
    });
  }

  async function drawFigure(figure, link, source) {
    const [left, top, right, bottom] = readCrop(figure);
    const page = await getPage(source.url.href, source.number);
    if (!figure.isConnected) return;

    const baseViewport = page.getViewport({ scale: 1 });
    const cropWidth = (right - left) * baseViewport.width;
    const cropHeight = (bottom - top) * baseViewport.height;
    const layoutWidth = Math.min(1040, Math.max(520, figure.clientWidth));
    const pixelRatio = Math.min(2, Math.max(1, window.devicePixelRatio || 1));
    const scale = Math.min(
      layoutWidth * pixelRatio / cropWidth,
      maxCanvasSide / Math.max(cropWidth, cropHeight),
      Math.sqrt(maxCanvasPixels / (cropWidth * cropHeight)),
      12
    );
    const canvas = document.createElement("canvas");
    canvas.width = Math.max(1, Math.floor(cropWidth * scale));
    canvas.height = Math.max(1, Math.floor(cropHeight * scale));
    canvas.className = "course-figure-canvas";
    canvas.style.cssText = "display:block;max-width:100%;height:auto;margin-inline:auto;";

    // Translate the page into a crop-sized canvas to avoid a full-page bitmap.
    await page.render({
      canvas,
      viewport: page.getViewport({ scale }),
      transform: [1, 0, 0, 1, -left * baseViewport.width * scale, -top * baseViewport.height * scale]
    }).promise;
    if (!figure.isConnected) return;

    const label = figure.querySelector("figcaption")?.textContent.trim() ||
      link.getAttribute("aria-label") || `课程课件第 ${source.number} 页的图示`;
    const linkLabel = link.textContent.trim() || "查看课件原图";
    if (!link.hasAttribute("aria-label")) link.setAttribute("aria-label", linkLabel);
    canvas.setAttribute("role", "img");
    canvas.setAttribute("aria-label", label);
    canvas.textContent = label;
    link.replaceChildren(canvas);
  }

  function enhance(figure, autoRender) {
    if (processedFigures.has(figure)) return;
    const link = figure.querySelector("a[href]");
    if (!link) return;
    processedFigures.add(figure);

    let source;
    try {
      source = readSource(figure);
    } catch {
      return;
    }
    if (autoRender) {
      drawFigure(figure, link, source).catch(() => {
        if (figure.isConnected) addNativePreview(figure, source);
      });
    } else {
      addNativePreview(figure, source);
    }
  }

  const observer = typeof IntersectionObserver === "function" ?
    new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        observer.unobserve(entry.target);
        if (entry.target.isConnected) enhance(entry.target, true);
      }
    }, { rootMargin: "160px 0px" }) : null;

  function scan() {
    observer?.disconnect();
    for (const figure of document.querySelectorAll(selector)) {
      if (processedFigures.has(figure)) continue;
      if (observer) observer.observe(figure);
      else enhance(figure, false);
    }
  }

  window[bootKey] = scan;
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan, { once: true });
  } else {
    scan();
  }
  if (typeof document$ !== "undefined" && typeof document$.subscribe === "function") {
    document$.subscribe(scan);
  }
})();
