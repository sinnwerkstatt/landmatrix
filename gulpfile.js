var gulp = require('gulp');
var livereload = require('gulp-livereload');
var watch = require('gulp-watch');


gulp.task('watch', function () {
    livereload.listen();

    gulp.watch('**/templates/**').on('change', livereload.changed);
    gulp.watch('**/media/css/**').on('change', livereload.changed);
    gulp.watch('**/maplandmatrix/**').on('change', livereload.changed);

});

gulp.task('default' , ['watch']); 
