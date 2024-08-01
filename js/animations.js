gsap.registerPlugin(ScrollTrigger);

// АНИМАЦИЯ ИНТЕРФЕЙСА
// Анимация навбара



gsap.to("#point-1 object svg .anchor", {
	scrollTrigger: {
		trigger: "#head",
		start: "50% 50%",
		toggleActions: "restart none none reverse"
	},
	fill: "#DD1144",
	stroke: "#DD1144"
});

// АНИМАЦИЯ ГОЛОВНОГО ЭКРАНА
// Анимация телефонов

headAnim = gsap.timeline({ delay: 0.7 });
headAnim.from("#phone-1", { yPercent: 100, ease: "expo.out", duration: 1 });
headAnim.from("#phone-2", { yPercent: 150, ease: "expo.out", duration: 1.07 }, "<");


// АНИМАЦИЯ ЭКРАНА ПРЕИМУЩЕСТВ
// Триггер при прокрутке

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

// Анимация плашек с описаниями

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