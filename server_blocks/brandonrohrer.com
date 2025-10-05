# Set up rate limiting. Create a "zone", a 1MB history of IP addresses
# that have made requests. On average, they should be making no more than
# 1 request per second.
limit_req_zone $binary_remote_addr zone=one:1m rate=1r/s;

server {
    root /var/www/brandonrohrer.com/html;
    index blog.html;

    server_name brandonrohrer.com www.brandonrohrer.com;

    access_log /var/log/nginx/brandonrohrer.com/access.log;
	error_log /var/log/nginx/brandonrohrer.com/error.log;

    limit_req zone=one burst=10 nodelay;
    limit_req_status 429;

    # Do some blocking for security

    # Disable dotfiles except for the .well-known directory
    location ~ /\.(?!well-known).* {
        deny all;
    }

	location ~ \.php$ {
	    deny all;
	}

	# Block access if someone is hunting for WordPress files
	location /wp-admin/ {
	    deny all;
	}
	location /wp-contents/ {
	    deny all;
	}
	location /wp-includes/ {
	    deny all;
	}

    # Try to reach varations of the requested file
	location / {
        try_files $uri $uri.html $uri/ =404;
	}

    # Forward all requests for images and videos to the Content Delivery Network
    # (in this case it's just GutHub)
	location ~ ^/images/(.*) {
	    return 301 https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/$1;
	}
	location ~ ^/videos/(.*) {
	    return 301 https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/$1;
	}

    ######################
    # Forwards

	location ~ ^/brohrer/sqlogging/(.*) {
	    return 301 https://github.com/brohrer/sqlogging/$1;
	}

	location = /httyr {
	     return 301 $scheme://brandonrohrer.com/httyr/httyr.html; 
	}
	location = /howtotrainyourrobot {
	     return 301 $scheme://brandonrohrer.com/httyr/httyr.html; 
	}
	location = /how_to_train_your_robot{
	     return 301 $scheme://brandonrohrer.com/httyr/httyr.html; 
	}
	location = /buckettree {
	     return 301 https://codeberg.org/brohrer/bucket-tree;
	}
	location = /cartographer {
	     return 301 https://codeberg.org/brohrer/cartographer-paper/raw/branch/main/cartographer.pdf;
	}
	location = /fnc {
	     return 301 https://codeberg.org/brohrer/cartographer-paper/raw/branch/main/cartographer.pdf;
	}
	location = /myrtle {
	     return 301 https://codeberg.org/brohrer/myrtle;
	}
	location = /numba {
	     return 301 $scheme://brandonrohrer.com/numba_tips.html;
	}
	location = /ziptie {
	     return 301 https://codeberg.org/brohrer/ziptie-paper/src/branch/main/ziptie.pdf;
	}

	location = /cottonwood {
	     return 301 https://gitlab.com/brohrer/cottonwood/;
	}
	location = /ponderosa {
	     return 301 https://gitlab.com/brohrer/ponderosa/;
	}
	location = /lodgepole {
	     return 301 https://gitlab.com/brohrer/lodgepole/;
	}
	location = /backpropagation {
	     return 301 https://www.youtube.com/watch?v=6BMwisTZFr4;
	}
	location = /backprop {
	     return 301 https://www.youtube.com/watch?v=6BMwisTZFr4;
	}
	location = /bp {
	     return 301 https://www.youtube.com/watch?v=6BMwisTZFr4;
	}

	location = /ecg {
	     return 301 https://gitlab.com/brohrer/study-ecg-rhythms;
	}
	location = /ecg-rhythms {
	     return 301 https://gitlab.com/brohrer/study-ecg-rhythms;
	}
	location = /ecgrhythms {
	     return 301 https://gitlab.com/brohrer/study-ecg-rhythms;
	}

	location = /mnist {
	     return 301 https://gitlab.com/brohrer/study-mnist-digits;
	}
	location = /mnist-digits {
	     return 301 https://gitlab.com/brohrer/study-mnist-digits;
	}
	location = /mnistdigits {
	     return 301 https://gitlab.com/brohrer/study-mnist-digits;
	}

	location = /cifar {
	     return 301 https://gitlab.com/brohrer/study-cifar-10;
	}
	location = /cifar-10 {
	     return 301 https://gitlab.com/brohrer/study-cifar-10;
	}
	location = /cifar10 {
	     return 301 https://gitlab.com/brohrer/study-cifar-10;
	}


	location = /data_replication {
	     return 301 https://github.com/brohrer/sqlogging;
	}
	location = /statistics_resources.html  {
	     return 301 /stats_resources.html;
	}

	location = /drugs {
	     return 301 https://docs.google.com/document/d/18NPpsxH9Z-x68KcrGzb7P3R1ucoNHP-95MKcAIy_Tsc/edit;
	}
	location = /rickroll {
	     return 301 https://vimeo.com/685995963  ;
	}

	location = /1 {
	     return 301 /httyr/httyr01.html;
	}
	location = /httyr1 {
	     return 301 /httyr/httyr01.html;
	}
	location = /httyr1pdf {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_1/chapter_1.pdf;
	}
	location = /httyr1book {
	     return 301 https://www.lulu.com/shop/brandon-rohrer/cant-artificial-intelligence-already-do-that/paperback/product-wddm7j.html?page=1&pageSize=4;
	}
	location = /httyr1files {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/tree/main/chapter_1 ;
	}

	location = /2 {
	     return 301 https://www.brandonrohrer.com/httyr/httyr02.html;    
	}
	location = /httyr2 {
	     return 301 https://www.brandonrohrer.com/httyr/httyr02.html;    
	}
	location = /httyr2pdf {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_2/chapter_2.pdf;
	}
	location = /httyr2files {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/tree/main/chapter_2;
	}

	location = /3 {
	     return 301 $scheme://brandonrohrer.com/httyr/httyr03.html;
	}
	location = /httyr3 {
	     return 301 $scheme://brandonrohrer.com/httyr/httyr03.html;
	}
	location = /httyr3pdf {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_3/chapter_3.pdf;
	}
	location = /httyr3book {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_3/chapter_3.pdf;
	}
	location = /httyr3files {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/tree/main/chapter_3;
	}

	location = /4 {
	     return 301 $scheme://brandonrohrer.com/httyr/httyr04.html;
	}
	location = /httyr4 {
	     return 301 $scheme://brandonrohrer.com/httyr/httyr04.html;
	}
	location = /httyr4pdf {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_4/chapter_4.pdf;
	}
	location = /httyr4book {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_4/chapter_4.pdf;
	}
	location = /httyr4files {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/tree/main/chapter_4;
	}

	location = /httyr4lissajous {
	     return 301 https://vimeo.com/760820897;
	}
	location = /4lissajous {
	     return 301 https://vimeo.com/760820897;
	}
	location = /httyr4shadows {
	     return 301 https://vimeo.com/763578113;
	}
	location = /4shadows {
	     return 301 https://vimeo.com/763578113;
	}
	location = /httyr4pulsing {
	     return 301 https://vimeo.com/765403954;
	}
	location = /4pulsing {
	     return 301 https://vimeo.com/765403954;
	}
	location = /httyr4rocking {
	     return 301 https://vimeo.com/765512127;
	}
	location = /4rocking {
	     return 301 https://vimeo.com/765512127;
	}
	location = /httyr4constant {
	     return 301 https://vimeo.com/768242153;
	}
	location = /4constant {
	     return 301 https://vimeo.com/768242153;
	}
	location = /httyr4triangular {
	     return 301 https://vimeo.com/768247848;
	}
	location = /4triangular {
	     return 301 https://vimeo.com/768247848;
	}
	location = /httyr4minjerk {
	     return 301 https://vimeo.com/768248726;
	}
	location = /4minjerk {
	     return 301 https://vimeo.com/768248726;
	}
	location = /httyr4logit {
	     return 301 https://vimeo.com/772902777;
	}
	location = /4logit {
	     return 301 https://vimeo.com/772902777;
	}
	location = /4logitnorm {
	     return 301 https://en.wikipedia.org/wiki/Logit-normal_distribution;
	}
	location = /4matmul {
	     return 301 https://brandonrohrer.com/transformers.html#matrix_multiplication;
	}
	location = /4color {
	     return 301 https://brandonrohrer.com/matplotlib_color.html;
	}
	location = /4numbers {
	     return 301 https://brandonrohrer.com/images_to_numbers.html;
	}
	location = /4matplotlib {
	     return 301 https://matplotlib.org/stable/api/index;
	}
	location = /4shadmehr {
	     return 301 http://courses.shadmehrlab.org/Shortcourse/minimumjerk.pdf;
	}
	location = /4plamondon {
	     return 301 http://diabeto.enseeiht.fr/download/handwriting/PlamonVelocity.pdf;
	}
	location = /4hogan {
	     return 301 https://summerschool.stiff-project.org/uploads/tx_sibibtex/Hogan_-_Adaptive_control_of_mechanical_impedance_by_coactivation_of_antagonist_muscles.pdf;
	}

	location = /httyr5 {
	     return 301 https://www.brandonrohrer.com/httyr/httyr05.html;
	}
	location = /httyr5pdf {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_5/chapter_5.pdf;
	}
	location = /5 {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_5/chapter_5.pdf;
	}
	location = /5pdf {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_5/chapter_5.pdf;
	}
	location = /httyr5files {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/tree/main/chapter_5;
	}
	location = /5files {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/tree/main/chapter_5;
	}
	location = /5plinko {
	     return 301 https://vimeo.com/789313997;  
	}

	location = /6 {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_6/chapter_6.pdf;
	}
	location = /httyr6 {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_6/chapter_6.pdf;
	}
	location = /httyr6pdf {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_6/chapter_6.pdf;
	}
	location = /6pdf {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/raw/main/chapter_6/chapter_6.pdf;
	}
	location = /httyr6files {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/tree/main/chapter_6;
	}
	location = /6files {
	     return 301 https://github.com/brohrer/how-to-train-your-robot/tree/main/chapter_6;
	}

    listen [::]:443 ssl; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/brandonrohrer.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/brandonrohrer.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}
server {
    if ($host = www.brandonrohrer.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    if ($host = brandonrohrer.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

        listen 80;
        listen [::]:80;

        server_name brandonrohrer.com www.brandonrohrer.com;
    return 404; # managed by Certbot
}

