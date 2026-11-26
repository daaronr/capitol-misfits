for (const card of document.querySelectorAll("[data-card]")) {
  const front = card.querySelector("[data-front]");
  const back = card.querySelector("[data-back]");
  const flip = card.querySelector("[data-flip]");
  back.hidden = true;
  flip.hidden = false;

  flip.addEventListener("click", () => {
    const showBack = back.hidden;
    back.hidden = !showBack;
    front.hidden = showBack;
    flip.setAttribute("aria-expanded", String(showBack));
    flip.textContent = showBack ? "Show front" : "Flip card";
  });
}

for (const button of document.querySelectorAll("[data-copy]")) {
  if (!navigator.clipboard?.writeText) continue;
  button.hidden = false;
  const status = button.parentElement.querySelector("[role=status]");
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(new URL(button.dataset.copy, document.baseURI).href);
      status.textContent = "Link copied.";
    } catch {
      status.textContent = "Open the card page to copy its address.";
    }
  });
}
