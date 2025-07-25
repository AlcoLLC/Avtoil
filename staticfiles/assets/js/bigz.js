$(function() {
    "use strict";
    
    $(window).on("load", function() {
        // Preloader
        $("#preloader").fadeOut(600);
        $(".preloader-bg").delay(400).fadeOut(600);
        
        // Show elements with fade in animation
        setTimeout(function() {
            $(".fadeIn-element").delay(1400).css({
                display: "none"
            }).fadeIn(1600);
        }, 0);
        
        // Show borders
        setTimeout(function() {
            $(".logo, #menu-mobile-btn").removeClass("top-position");
        }, 800);
        setTimeout(function() {
            $(".social-icons-launcher, .progress-clock").removeClass("bottom-position");
        }, 800);
        
        // Show hero background
        $(".hero-bg").addClass("hero-bg-show");
    });
    
    // Navigation highlight
    $("a.menu-state").on("click", function() {
        $("a.menu-state").removeClass("active");
        $(this).addClass("active");
    });
    
    // Scroll to top arrow
    $(window).on("scroll", function() {
        if ($(this).scrollTop() > 100) {
            $(".to-top-arrow").addClass("show");
        } else {
            $(".to-top-arrow").removeClass("show");
        }
    });
    
    // Scroll to top functionality
    $(".scrollToTop, #menu-mobile-btn").on("click", function() {
        $("html, body").animate({
            scrollTop: 0
        }, 800);
        return false;
    });
    
    // Menu launcher
    $("#menu-mobile-btn").on("click", function() {
        if ($(".introduction").hasClass("introduction-off")) {
            $(".introduction").removeClass("introduction-off").addClass("introduction-on");
            $("nav.navigation-menu").removeClass("show");
        } else {
            $(".introduction").removeClass("introduction-on").addClass("introduction-off");
            $("nav.navigation-menu").addClass("show");
        }
    });
    
    // Navigation menu
    $("nav.navigation-menu a").on("click", function() {
        if ($("nav.navigation-menu").hasClass("show")) {
            $("nav.navigation-menu").removeClass("show");
            $(".introduction").removeClass("introduction-off").addClass("introduction-on");
        } else {
            $("nav.navigation-menu").addClass("show");
        }
    });
    
    // Navigation hover effects
    $(".menu li a").on("mouseenter", function() {
        var ref = $(this).data("ref"),
            menuImg = $('.menu-img[data-ref="' + ref + '"]');
        $(".menu li a").removeClass("active");
        $(this).addClass("active");
        $(".menu-img").removeClass("active");
        menuImg.addClass("active");
    });
    
    // Background images
    $("[data-bg]").each(function() {
        var bg = $(this).data("bg");
        $(this).css({
            "background-image": 'url(' + bg + ')',
            "background-position": "center center",
            "background-size": "cover"
        });
    });
    
    // Line animation
    $(".line-box").on("mouseenter", function() {
        $(this).addClass("animated");
        setTimeout(function() {
            $(".animated").removeClass("animated")
        }, 2000);
    });
    
    // "Not Found" button redirect to home page
    $(".the-button").on("click", function() {
        if ($(this).text() === "Not Found") {
            window.location.href = "/"; // Ana sayfaya yönlendir
        }
    });
    
});