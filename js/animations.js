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


// АНИМАЦИЯ ГОЛОВНОГО ЭКРАНА (PC/Phone)

headHidePhonesTriggerPC = ScrollTrigger.create({
	trigger: "#head",
	start: "80% 10%",
	end: "80% 10%",
	onEnter: () => {headHidePhonesAnimPC.reverse();},
	onEnterBack: () => {headHidePhonesAnimPC.restart();}
});

headOnStartAnim = gsap.timeline();
headOnStartAnim.add(headOnStartAnimPC);
headOnStartAnim.addLabel("pc", "<");
headOnStartAnim.add(headOnStartAnimMobile);
headOnStartAnim.addLabel("mobile", "<");
headOnStartAnim.addPause("mobile");
headOnStartAnim.addPause(">");

headOnStartAnimPC = gsap.timeline().pause();
headOnStartAnimPC.from("#phone-1", { yPercent: 100, ease: "expo.out", duration: 1 });
headOnStartAnimPC.from("#phone-2", { yPercent: 150, ease: "expo.out", duration: 1.07 }, "<");
headOnStartAnimPC.from("#head-title", { xPercent: -100, ease: "expo.out", duration: 1.07 }, "<");
headOnStartAnimPC.from("#download-1", { yPercent: 170, ease: "expo.out", duration: 1.07 }, "<");

headHidePhonesAnimPC = gsap.timeline();
headHidePhonesAnimPC.from("#phone-1", { xPercent: -160, ease: "expo.out", duration: 0.5 });
headHidePhonesAnimPC.from("#phone-2", { xPercent: -160, ease: "expo.out", duration: 0.5 }, "<");

headHidePhonesTriggerMobile = ScrollTrigger.create({
	trigger: "#head",
	start: "80% 10%",
	end: "80% 10%",
	onEnter: () => {headHidePhonesAnimMobile.reverse();},
	onEnterBack: () => {headHidePhonesAnimMobile.restart();}
});

headOnStartAnimMobile = gsap.timeline().pause();
headOnStartAnimMobile.from("#phones-mobile", { yPercent: 100, ease: "expo.out", duration: 1 });
headOnStartAnimMobile.from("#head-title", { xPercent: 100, ease: "expo.out", duration: 1.07 }, "<");
headOnStartAnimMobile.from("#download-1", { yPercent: 170, ease: "expo.out", duration: 1.07 }, "<");

// АНИМАЦИЯ ЭКРАНА ПРЕИМУЩЕСТВ
// Анимация секции при прокрутке

advantagesAnimTriggerPC = ScrollTrigger.create({
	trigger: "#our-advantage",
	start: "top 30%",
	onEnter: () => {advantagesAnimPC.play();}
});

advantagesAnimPC = gsap.timeline();
advantagesAnimPC.from(".overflow-wrapper h2", { yPercent: -100, opacity: 0, duration: 1 });
advantagesAnimPC.to("#advantages", { rowGap: 120, duration: 0.7 }, "<");
advantagesAnimPC.to(".description-item:nth-child(even)", { xPercent: 27, duration: 0.7 }, "<");
advantagesAnimPC.to(".description-item:nth-child(odd)", { xPercent: -27, duration: 0.7 }, "<");

// Анимация плашек с описаниями (PC)

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


// АНИМАЦИЯ РОГА
hornAnimTriggerPC = ScrollTrigger.create({
	trigger: "#horn",
	start: "top 70%",
	onEnter: () => {hornAnimPC.play();},
	once: true
});

hornAnimPC = gsap.from("#horn", {
	yPercent: 150,
	duration: 0.7,
	ease: "power4.out"
});

// АНИМАЦИЯ ХВОСТОВОГО ЗАГОЛОВКА (PC)

tailOnScrollAnimTriggerPC = ScrollTrigger.create({
	trigger: ".tail-coloriser",
	start: "30% 10%",
	onEnter: () => {tailOnScrollAnimPC.play();},
	once: true
});

tailOnScrollAnimPC = gsap.timeline();
tailOnScrollAnimPC.from("#phone-4", { yPercent: 110, ease: "expo.out", duration: 1 });
tailOnScrollAnimPC.from("#tail-title", { xPercent: -100, ease: "expo.out", duration: 1.07 }, "<");
tailOnScrollAnimPC.from("#download-2", { yPercent: 170, ease: "expo.out", duration: 1.07 }, "<");

tailHidePhoneTriggerPC = ScrollTrigger.create({
	trigger: "#tail",
	start: "50% 70%",
	end: "50% 70%",
	onEnter: () => {tailHidePhoneAnimPC.reverse();},
	onEnterBack: () => {tailHidePhoneAnimPC.restart();}
});

tailHidePhoneAnimPC = gsap.timeline();
tailHidePhoneAnimPC.to("#phone-4", { xPercent: -150, ease: "expo.in", duration: 0.5 });



// УПРАВЛЕНИЕ РАЗРЕШЕНИЯМИ ЭКРАНОВ

if (window.matchMedia('(min-width: 1024px)').matches) {
	window.addEventListener('load', () => {
		headOnStartAnim.seek("pc").restart();
	});
} else {
	headHidePhonesTriggerPC.disable();
	window.addEventListener('load', () => {
		headOnStartAnim.seek("mobile").restart();
	});
}

window.addEventListener("resize", () => {
	if (window.matchMedia('(min-width: 1024px)').matches) {
		
	} else {
		
	}
});