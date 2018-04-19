$(document).ready(function(){
    <!-- Sidebar toggle -->
	var $menu = $('.sidebar-toggle');
	var $logo = $('.logo');
	var $sidebar = $('.main-sidebar');
	var $topBtn = $('.back-to-top-btn');
	var $content = $('.page-content');
	var $breadcrumbs = $('.breadcrumbs-wrapper');
	var $footer = $('footer');
	$menu.click(function(e) {
		e.preventDefault(); // don't scroll to top on sidebar open
		$menu.toggleClass('sidebar-toggle-toggled');
		$logo.toggleClass('full');
		$sidebar.toggleClass('active');
		$topBtn.toggleClass('active');
		$content.toggleClass('active');
		$breadcrumbs.toggleClass('active');
		$footer.toggleClass('active');
	});

	<!-- Scroll to top button -->
	var $btn = $('.back-to-top-btn');
	$(window).scroll(function(){
		if ($(this).scrollTop() > 300) {
			$btn.fadeIn();
		} else {
			$btn.fadeOut();
		}
	});
    $btn.click(function(){
        $('html, body').animate({scrollTop : 0}, 800);
        return false;
    });
});