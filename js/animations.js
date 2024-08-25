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
			if (window.matchMedia('(min-width: 1024px)').matches) {
				lineHeight = "21vh";
			} else {
				lineHeight = "17vh"
			}
			break;
		case 5:
			lineType = "bracket";
			if (window.matchMedia('(min-width: 1024px)').matches) {
				lineHeight = "21vh";
			} else {
				lineHeight = "17vh"
			}
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
	navMenuAnim.to(`#nav-${sections[i]} .nav-description`, { color: "#DD1144" }, "<");
	try {
		svgObj.addEventListener("load", () => {
			var svgDoc = svgObj.contentDocument;
			var svgImage = svgDoc.querySelector(".anchor");
			navMenuAnim.to(svgImage, { fill: "#DD1144", stroke: "#DD1144" });
		});
	} catch {
		
	}
}

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

// УПРАВЛЕНИЕ РАЗРЕШЕНИЯМИ ЭКРАНОВ

if (window.matchMedia('(min-width: 1024px)').matches) {
	window.addEventListener('load', () => {

		headHidePhonesTriggerPC = ScrollTrigger.create({
			trigger: "#head",
			start: "80% 10%",
			end: "80% 10%",
			onEnter: () => {headHidePhonesAnimPC.reverse();},
			onEnterBack: () => {headHidePhonesAnimPC.restart();}
		});

		advantagesAnimTriggerPC = ScrollTrigger.create({
			trigger: "#our-advantage",
			start: "top 20%",
			onEnter: () => {advantagesAnimPC.play();},
			once: true
		});

		whatIsAnimTriggerPC = ScrollTrigger.create({
			trigger: "#what-is",
			start: "top top",
			onEnter: () => {whatIsAnimPC.play();},
			once: true
		});

		buyTokensAnimTriggerPC = ScrollTrigger.create({
			trigger: "#buy-tokens",
			start: "top top",
			onEnter: () => {buyTokensAnimPC.play();},
			once: true
		});

		hornAnimTriggerPC = ScrollTrigger.create({
			trigger: "#horn",
			start: "top 30%",
			onEnter: () => {hornAnimPC.play();},
			once: true
		});

		tailOnScrollAnimTriggerPC = ScrollTrigger.create({
			trigger: ".tail-coloriser",
			start: "30% 10%",
			onEnter: () => {tailOnScrollAnimPC.play();},
			once: true
		});

		tailHidePhoneTriggerPC = ScrollTrigger.create({
			trigger: "#tail",
			start: "50% 70%",
			end: "50% 70%",
			onEnter: () => {tailHidePhoneAnimPC.reverse();},
			onEnterBack: () => {tailHidePhoneAnimPC.restart();}
		});

		headOnStartAnimPC = gsap.timeline();
		headOnStartAnimPC.from("#phone-1", { yPercent: 100, ease: "expo.out", duration: 1 });
		headOnStartAnimPC.from("#phone-2", { yPercent: 150, ease: "expo.out", duration: 1.07 }, "<");
		headOnStartAnimPC.from("#head-title", { xPercent: -100, ease: "expo.out", duration: 1.07 }, "<");
		headOnStartAnimPC.from("#download-1", { yPercent: 170, ease: "expo.out", duration: 1.07 }, "<");
		headOnStartAnimPC.from("#nav", { opacity: 0, ease: "expo.out", duration: 2 }, "<");
		
		headOnStartAnimPC.restart();

		headHidePhonesAnimPC = gsap.timeline();
		headHidePhonesAnimPC.from("#phone-1", { xPercent: -220, ease: "expo.out", duration: 0.5 });
		headHidePhonesAnimPC.from("#phone-2", { xPercent: -220, ease: "expo.out", duration: 0.5 }, "<");

		whatIsAnimPC = gsap.timeline().pause();
		whatIsAnimPC.from("#what-is h2", { yPercent: -100, opacity: 0, ease: "expo.out", duration: 1.5});
		whatIsAnimPC.from("#what-is p", { yPercent: 30, opacity: 0, ease: "expo.out", duration: 1});

		advantagesAnimPC = gsap.timeline().pause();
		advantagesAnimPC.from(".overflow-wrapper h2", { yPercent: -100, opacity: 0, duration: 1 });
		advantagesAnimPC.to("#advantages", { rowGap: 120, duration: 0.7 }, "<");
		advantagesAnimPC.to(".description-item:nth-child(even)", { xPercent: 27, duration: 0.7 }, "<");
		advantagesAnimPC.to(".description-item:nth-child(odd)", { xPercent: -27, duration: 0.7 }, "<");

		buyTokensAnimPC = gsap.timeline().pause();
		buyTokensAnimPC.from(".buy-tokens__title", { yPercent: -30, opacity: 0, ease: "expo.out", duration: 0.7});
		buyTokensAnimPC.from(".buy-tokens-form", { yPercent: 100, opacity: 0, ease: "expo.out", duration: 1});
		buyTokensAnimPC.from(".tokens-description", { yPercent: 100, opacity: 0, ease: "expo.out", duration: 1}, "<");

		hornAnimPC = gsap.from("#horn", {
			yPercent: 150,
			duration: 0.7,
			ease: "power4.out"
		}).pause();

		tailOnScrollAnimPC = gsap.timeline().pause();
		tailOnScrollAnimPC.from("#phone-4", { yPercent: 110, ease: "expo.out", duration: 1 });
		tailOnScrollAnimPC.from("#tail-title", { xPercent: -100, ease: "expo.out", duration: 1.07 }, "<");
		tailOnScrollAnimPC.from("#download-2", { yPercent: 170, ease: "expo.out", duration: 1.07 }, "<");

		tailHidePhoneAnimPC = gsap.timeline();
		tailHidePhoneAnimPC.to("#phone-4", { xPercent: -150, ease: "expo.in", duration: 0.5 });

		accountAnimPC = gsap.timeline().pause();
		accountAnimPC.to(".account-navbar-menu", { opacity: 1, y: 596, ease: "expo.inout", duration: 0.5 });
		accountAnimPC.to(".account-navbar-menu-exit", { backgroundColor: "#00000040", pointerEvents: "all", ease: "power2.inout", duration: 0.4 }, "<");

		document.querySelector(".account-navbar-menu-exit").addEventListener("mousedown", () => {
			accountAnimPC.reverse();
		});

		document.querySelector("#account-navbar-auth .account-wrapper").addEventListener("mousedown", () => {
			accountAnimPC.restart();
		});
		
	});

} else if (window.matchMedia('(min-width: 601px)').matches) {
	window.addEventListener('load', () => {

		whatIsAnimTriggerMobile = ScrollTrigger.create({
			trigger: "#what-is",
			start: "top 30%",
			onEnter: () => {whatIsAnimMobile.play();},
			once: true
		});

		advantagesAnimTriggerMobile = ScrollTrigger.create({
			trigger: "#our-advantage",
			start: "top 30%",
			onEnter: () => {advantagesAnimMobile.play();},
			once: true
		});

		buyTokensAnimTriggerMobile = ScrollTrigger.create({
			trigger: "#buy-tokens",
			start: "top 30%",
			onEnter: () => {buyTokensAnimMobile.play();},
			once: true
		});

		tailAnimTriggerMobile = ScrollTrigger.create({
			trigger: "#tail",
			start: "top 30%",
			onEnter: () => {tailAnimMobile.play();},
			once: true
		});

		headOnStartAnimMobile = gsap.timeline();
		headOnStartAnimMobile.from("#phones-mobile", { yPercent: 100, ease: "expo.out", duration: 1 });
		headOnStartAnimMobile.from("#head-title", { width: 0, paddingRight: 0, ease: "expo.out", duration: 1.07 }, "<");
		headOnStartAnimMobile.from("#download-1", { yPercent: 100, ease: "expo.out", duration: 1.07 }, "<");
		headOnStartAnimMobile.from(".account-navbar", { yPercent: -200, ease: "expo.out", duration: 1.07 }, "<");

		navAnimMobile = gsap.timeline().pause();
		navAnimMobile.set(".nav-description", { minWidth: "40vw" });
		navAnimMobile.to("#nav", { width: "60vw", ease: "expo.inout", duration: 0.5 });
		navAnimMobile.from(".nav-wrapper", { backgroundColor: "#00000011", pointerEvents: "none", ease: "power2.inout", duration: 0.4 }, "<");
		navAnimMobile.set(".nav-description", { minWidth: "fit-content" });

		whatIsAnimMobile = gsap.timeline().pause();
		whatIsAnimMobile.from("#what-is h2", { yPercent: 900, duration: 1, ease: "expo.out" });
		whatIsAnimMobile.from(".phone__what-is", { yPercent: 200, opacity: 0, duration: 1, ease: "expo.out" }, "<");
		whatIsAnimMobile.from("#what-is p", { yPercent: 200, opacity: 0, duration: 1, ease: "expo.out" });

		advantagesAnimMobile = gsap.timeline().pause();
		advantagesAnimMobile.from("#advantages-mobile", { xPercent: -70, yPercent: 100, duration: 1, ease: "expo.out" });
		advantagesAnimMobile.from("#phone-3", { xPercent: 100, yPercent: 200, opacity: 0, duration: 1, ease: "expo.out" });

		buyTokensAnimMobile = gsap.timeline().pause();
		buyTokensAnimMobile.from(".buy-tokens__title", { yPercent: 200, opacity: 0, duration: 1, ease: "expo.out" });
		buyTokensAnimMobile.from(".buy-tokens-form", { xPercent: -200, opacity: 0, duration: 1, ease: "expo.out" });
		buyTokensAnimMobile.from(".tokens-description", { xPercent: -200, opacity: 0, duration: 1, ease: "expo.out" }, "<");

		tailAnimMobile = gsap.timeline().pause();
		tailAnimMobile.from("#phone-4", { yPercent: 100, ease: "expo.out", duration: 1 });
		tailAnimMobile.from("#tail-title", { width: 0, paddingRight: 0, ease: "expo.out", duration: 1.07 }, "<");
		tailAnimMobile.from("#download-2", { yPercent: 100, ease: "expo.out", duration: 1.07 }, "<");

		document.querySelector(".nav-wrapper").addEventListener("mousedown", () => {
			navAnimMobile.reverse();
		});

		gsap.utils.toArray(".partitions-image__wrapper").forEach(partitions => {
			partitions.addEventListener("mousedown", () => {
				navAnimMobile.play();
			});
		});

		accountAnimMobile = gsap.timeline().pause();
		accountAnimMobile.from(".account-navbar-menu", { opacity: 0, yPercent: 200, ease: "expo.inout", duration: 0.5 });
		accountAnimMobile.to(".account-navbar-menu-exit", { backgroundColor: "#00000040", pointerEvents: "all", ease: "power2.inout", duration: 0.4 }, "<");

		document.querySelector(".account-navbar-menu-exit").addEventListener("mousedown", () => {
			accountAnimMobile.reverse();
		});

		document.querySelector("#account-navbar-auth .account-wrapper").addEventListener("mousedown", () => {
			accountAnimMobile.restart();
		});

	});

} else if (window.matchMedia('(min-width: 340px)').matches) {
	window.addEventListener('load', () => {

		whatIsAnimTriggerMobile = ScrollTrigger.create({
			trigger: "#what-is",
			start: "top 30%",
			onEnter: () => {whatIsAnimMobile.play();},
			once: true
		});

		advantagesAnimTriggerMobile = ScrollTrigger.create({
			trigger: "#our-advantage",
			start: "top 30%",
			onEnter: () => {advantagesAnimMobile.play();},
			once: true
		});

		buyTokensAnimTriggerMobile = ScrollTrigger.create({
			trigger: "#buy-tokens",
			start: "top 30%",
			onEnter: () => {buyTokensAnimMobile.play();},
			once: true
		});

		tailAnimTriggerMobile = ScrollTrigger.create({
			trigger: "#tail",
			start: "top 30%",
			onEnter: () => {tailAnimMobile.play();},
			once: true
		});

		headOnStartAnimMobile = gsap.timeline();
		headOnStartAnimMobile.from("#phones-mobile", { yPercent: 100, ease: "expo.out", duration: 1 });
		headOnStartAnimMobile.from("#head-title", { width: 0, paddingRight: 0, ease: "expo.out", duration: 1.07 }, "<");
		headOnStartAnimMobile.from("#download-1", { yPercent: 100, ease: "expo.out", duration: 1.07 }, "<");
		headOnStartAnimMobile.from(".account-navbar", { yPercent: -200, ease: "expo.out", duration: 1.07 }, "<");

		navAnimMobile = gsap.timeline().pause();
		navAnimMobile.set(".nav-description", { minWidth: "60vw" });
		navAnimMobile.to(".nav-wrapper", { opacity: 1, backgroundColor: "#00000011", pointerEvents: "all" }, "<");
		navAnimMobile.set(".nav-description", { minWidth: "fit-content" });

		whatIsAnimMobile = gsap.timeline().pause();
		whatIsAnimMobile.from("#what-is h2", { yPercent: 900, duration: 1, ease: "expo.out" });
		whatIsAnimMobile.from(".phone__what-is", { yPercent: 200, opacity: 0, duration: 1, ease: "expo.out" }, "<");
		whatIsAnimMobile.from("#what-is p", { yPercent: 200, opacity: 0, duration: 1, ease: "expo.out" });

		advantagesAnimMobile = gsap.timeline().pause();
		advantagesAnimMobile.from("#phone-3", { xPercent: -70, yPercent: 200, opacity: 0, duration: 1, ease: "expo.out" });
		advantagesAnimMobile.from("#advantages-mobile", { xPercent: -70, yPercent: 100, duration: 1, ease: "expo.out" });

		buyTokensAnimMobile = gsap.timeline().pause();
		buyTokensAnimMobile.from(".buy-tokens__title", { yPercent: 200, opacity: 0, duration: 1, ease: "expo.out" });
		buyTokensAnimMobile.from(".buy-tokens-form", { xPercent: -200, opacity: 0, duration: 1, ease: "expo.out" });
		buyTokensAnimMobile.from(".tokens-description", { xPercent: -200, opacity: 0, duration: 1, ease: "expo.out" }, "<");

		tailAnimMobile = gsap.timeline().pause();
		tailAnimMobile.from("#phone-4", { yPercent: 100, ease: "expo.out", duration: 1 });
		tailAnimMobile.from("#tail-title", { xPercent: -150, ease: "expo.out", duration: 1 }, "<");
		tailAnimMobile.from("#download-2", { yPercent: 100, ease: "expo.out", duration: 1.07 }, "<");

		document.querySelector(".nav-wrapper").addEventListener("mousedown", () => {
			navAnimMobile.reverse();
		});

		gsap.utils.toArray(".partitions-image__wrapper").forEach(partitions => {
			partitions.addEventListener("mousedown", () => {
				navAnimMobile.play();
			});
		});

		accountAnimMobile = gsap.timeline().pause();
		accountAnimMobile.from(".account-navbar-menu", { opacity: 0, yPercent: 200, ease: "expo.inout", duration: 0.5 });
		accountAnimMobile.to(".account-navbar-menu-exit", { backgroundColor: "#00000040", pointerEvents: "all", ease: "power2.inout", duration: 0.4 }, "<");

		document.querySelector(".account-navbar-menu-exit").addEventListener("mousedown", () => {
			accountAnimMobile.reverse();
		});

		document.querySelector("#account-navbar-auth .account-wrapper").addEventListener("mousedown", () => {
			accountAnimMobile.restart();
		});

	});
} else {
	window.addEventListener('load', () => {

		whatIsAnimTriggerMobile = ScrollTrigger.create({
			trigger: "#what-is",
			start: "top 30%",
			onEnter: () => {whatIsAnimMobile.play();},
			once: true
		});

		advantagesAnimTriggerMobile = ScrollTrigger.create({
			trigger: "#our-advantage",
			start: "top 30%",
			onEnter: () => {advantagesAnimMobile.play();},
			once: true
		});

		buyTokensAnimTriggerMobile = ScrollTrigger.create({
			trigger: "#buy-tokens",
			start: "top 30%",
			onEnter: () => {buyTokensAnimMobile.play();},
			once: true
		});

		tailAnimTriggerMobile = ScrollTrigger.create({
			trigger: "#tail",
			start: "top 30%",
			onEnter: () => {tailAnimMobile.play();},
			once: true
		});

		headOnStartAnimMobile = gsap.timeline();
		headOnStartAnimMobile.from("#head-title", { width: 0, paddingRight: 0, ease: "expo.out", duration: 1.07 }, "<");
		headOnStartAnimMobile.from("#download-1", { yPercent: 100, ease: "expo.out", duration: 1.07 }, "<");
		headOnStartAnimMobile.from(".account-navbar", { yPercent: -200, ease: "expo.out", duration: 1.07 }, "<");

		navAnimMobile = gsap.timeline().pause();
		navAnimMobile.set(".nav-description", { minWidth: "60vw" });
		navAnimMobile.to(".nav-wrapper", { opacity: 1, backgroundColor: "#00000011", pointerEvents: "all" }, "<");
		navAnimMobile.set(".nav-description", { minWidth: "fit-content" });

		whatIsAnimMobile = gsap.timeline().pause();
		whatIsAnimMobile.from("#what-is h2", { yPercent: 900, duration: 1, ease: "expo.out" });
		whatIsAnimMobile.from(".phone__what-is", { yPercent: 200, opacity: 0, duration: 1, ease: "expo.out" }, "<");
		whatIsAnimMobile.from("#what-is p", { yPercent: 200, opacity: 0, duration: 1, ease: "expo.out" });

		advantagesAnimMobile = gsap.timeline().pause();
		advantagesAnimMobile.from("#phone-3", { xPercent: -70, yPercent: 200, opacity: 0, duration: 1, ease: "expo.out" });
		advantagesAnimMobile.from("#advantages-mobile", { xPercent: -70, yPercent: 100, duration: 1, ease: "expo.out" });

		buyTokensAnimMobile = gsap.timeline().pause();
		buyTokensAnimMobile.from(".buy-tokens__title", { yPercent: 200, opacity: 0, duration: 1, ease: "expo.out" });
		buyTokensAnimMobile.from(".buy-tokens-form", { xPercent: -200, opacity: 0, duration: 1, ease: "expo.out" });
		buyTokensAnimMobile.from(".tokens-description", { xPercent: -200, opacity: 0, duration: 1, ease: "expo.out" }, "<");

		tailAnimMobile = gsap.timeline().pause();
		tailAnimMobile.from("#tail-title", { width: 0, paddingRight: 0, ease: "expo.out", duration: 1.07 }, "<");
		tailAnimMobile.from("#download-2", { yPercent: 100, ease: "expo.out", duration: 1.07 }, "<");

		document.querySelector(".nav-wrapper").addEventListener("mousedown", () => {
			navAnimMobile.reverse();
		});

		gsap.utils.toArray(".partitions-image__wrapper").forEach(partitions => {
			partitions.addEventListener("mousedown", () => {
				navAnimMobile.play();
			});
		});

		accountAnimMobile = gsap.timeline().pause();
		accountAnimMobile.from(".account-navbar-menu", { opacity: 0, yPercent: 200, ease: "expo.inout", duration: 0.5 });
		accountAnimMobile.to(".account-navbar-menu-exit", { backgroundColor: "#00000040", pointerEvents: "all", ease: "power2.inout", duration: 0.4 }, "<");

		document.querySelector(".account-navbar-menu-exit").addEventListener("mousedown", () => {
			accountAnimMobile.reverse();
		});

		document.querySelector("#account-navbar-auth .account-wrapper").addEventListener("mousedown", () => {
			accountAnimMobile.restart();
		});
	});
} 