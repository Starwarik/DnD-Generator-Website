gsap.registerPlugin(ScrollTrigger);

advantagesAnim = gsap.timeline( {
	scrollTrigger: {
		trigger: "#our-advantage",
		start: "top 30%"
	}
});
advantagesAnim.from(".overflow-wrapper h2", { yPercent: -100, opacity: 0, duration: 1 });
advantagesAnim.to("#advantages", { rowGap: 120, duration: 0.7 }, "<");
advantagesAnim.to(".description-item:nth-child(even)", { xPercent: 27, duration: 0.7 }, "<");
advantagesAnim.to(".description-item:nth-child(odd)", { xPercent: -27, duration: 0.7 }, "<");

gsap.utils.toArray(".description-item").forEach(description => {
	let header = description.querySelector("dt"),
			text = description.querySelector("dd"),
			arrow = description.querySelector(".see-more-arrow"),
			tl = gsap.timeline({ paused: true });

	tl.to(description, { width: "69%" });
	tl.to(header, { yPercent: -30 }, "<");
	tl.to(text, { opacity: 1, height: "auto" }, "<");
	tl.to(arrow, { opacity: 0 }, "<");

	description.addEventListener("mouseenter", () =>
	tl.timeScale(1).play());

	description.addEventListener("mouseleave", () =>
		tl.timeScale(1).reverse());

});