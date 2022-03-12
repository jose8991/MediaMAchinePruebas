mysql -u$WP_DB_USER -p$WP_DB_PWD -e "CREATE DATABASE replicator;"
mysql -u$WP_DB_USER -p$WP_DB_PWD -e "CREATE USER replicator@localhost IDENTIFIED BY 'replicator2022';"
mysql -u$WP_DB_USER -p$WP_DB_PWD -e "GRANT ALL PRIVILEGES ON replicator.* TO replicator@localhost;"
mysql -u$WP_DB_USER -p$WP_DB_PWD -e "USE replicator; CREATE TABLE posts (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,instagram VARCHAR(128) NOT NULL,instagram_post_date VARCHAR(60) NOT NULL,wordpress_post_id VARCHAR(50),creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);"
