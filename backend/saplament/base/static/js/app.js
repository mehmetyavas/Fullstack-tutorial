const swiperThumbnail = new Swiper('.swiper-thumbnail', {
    slidesPerView: 4,
    spaceBetween: 30,
    loop: true,
    slideToClickedSlide: true
})

const swiperTop = new Swiper('.swiper-top', {
    autoplay: {
        delay: 5000
    },
    pauseOnMouseEnter: true,
    thumbs: {
        swiper: swiperThumbnail
    },
    loop: true,
})
