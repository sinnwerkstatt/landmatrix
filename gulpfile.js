var gulp = require('gulp');
var livereload = require('gulp-livereload');
var watch = require('gulp-watch');


gulp.task('watch', function () {
    livereload.listen();

    gulp.watch('**/templates/**', { interval: 1000 }).on('change', livereload.changed);
    gulp.watch('**/landmatrix/static/css/**', { interval: 1000 }).on('change', livereload.changed);
    gulp.watch('**/landmatrix/static/js/**', { interval: 1000 }).on('change', livereload.changed);
    gulp.watch('**/maplandmatrix/**', { interval: 1000 }).on('change', livereload.changed);

});

gulp.task('default' , ['watch']); 
