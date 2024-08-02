gsap.registerPlugin(ScrollTrigger);

// АНИМАЦИЯ ИНТЕРФЕЙСА
// Анимация навбара

let navMenus = gsap.utils.toArray(".navmenu");
let sections = [
	"head",
	"what-is",
	"our-advantage",
	"buy-tokens",
	"tail",
	"footer"];
let lineType = "";
let lineHeight = "";

for (let i = 0; i < navMenus.length; i++) {
	switch (i) {
		case 0:
			lineType = "bracket";
			lineHeight = "21vh";
			break;
		case 5:
			lineType = "bracket";
			lineHeight = "21vh";
			break;
		default:
			lineType = "middle";
			lineHeight = "13vh";
			break;
	}
	let navmenu = navMenus[i];
	let svgObj = navmenu.querySelector(".navpoint .navstar");
	let navMenuAnim = gsap.timeline({
		scrollTrigger: {
			trigger: `#${sections[i]}`,
			start: "500px 70%",
			toggleActions: "restart none none reverse"
		},
	});
	navMenuAnim.to(`#nav-${sections[i]} .${lineType}-line`, { borderTopWidth: `${lineHeight}` });
	try {
		svgObj.addEventListener("load", () => {
			var svgDoc = svgObj.contentDocument;
			var svgImage = svgDoc.querySelector(".anchor");
			navMenuAnim.to(svgImage, { fill: "#DD1144", stroke: "#DD1144" });
		});
	} catch {
		
	}
}

// АНИМАЦИЯ ГОЛОВНОГО ЭКРАНА

headOnStartAnim = gsap.timeline({ delay: 0.7 });
headOnStartAnim.from("#phone-1", { yPercent: 100, ease: "expo.out", duration: 1 });
headOnStartAnim.from("#phone-2", { yPercent: 150, ease: "expo.out", duration: 1.07 }, "<");
headOnStartAnim.from("#head-title", { xPercent: -100, ease: "expo.out", duration: 1.07 }, "<");
headOnStartAnim.from("#download-1", { yPercent: 170, ease: "expo.out", duration: 1.07 }, "<");

headHidePhonesAnim = gsap.timeline({
	scrollTrigger: {
		trigger: "#head",
		start: "80% 10%",
		end: "80% 10%",
		toggleActions: "restart none reverse none"
	}
})
headHidePhonesAnim.to("#phone-1", { xPercent: -160, ease: "expo.in", duration: 0.5 });
headHidePhonesAnim.to("#phone-2", { xPercent: -160, ease: "expo.in", duration: 0.5 }, "<");

// АНИМАЦИЯ ЭКРАНА ПРЕИМУЩЕСТВ
// Анимация секции при прокрутке

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

// АНИМАЦИЯ ХВОСТОВОГО ЗАГОЛОВКА

tailOnScrollAnim = gsap.timeline({ 
	scrollTrigger: {
		trigger: ".tail-coloriser",
		start: "30% 10%"
	}
 });
tailOnScrollAnim.from("#phone-4", { yPercent: 110, ease: "expo.out", duration: 1 });
tailOnScrollAnim.from("#tail-title", { xPercent: -100, ease: "expo.out", duration: 1.07 }, "<");
tailOnScrollAnim.from("#download-2", { yPercent: 170, ease: "expo.out", duration: 1.07 }, "<");

tailHidePhoneAnim = gsap.timeline({
	scrollTrigger: {
		trigger: "#tail",
		start: "50% 70%",
		end: "50% 70%",
		toggleActions: "reverse none restart none"
	}
});
tailHidePhoneAnim.to("#phone-4", { xPercent: -150, ease: "expo.in", duration: 0.5 });