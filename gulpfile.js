'use strict';

var gulp = require('gulp');
var concat = require('gulp-concat')
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');

gulp.task('compile-sass', function () {
    return gulp.src('assets/scss/main.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(autoprefixer({
            overrideBrowserslist: ['last 10 versions'],
            cascade: false
        }))
        .pipe(gulp.dest('assets/css'));
});

gulp.task('pack-css', function () {
    return gulp.src([
        'assets/css/vendors/jquery-ui.css',
        'assets/css/main.css',
    ])
        .pipe(concat('bundle.css'))
        .pipe(gulp.dest('public/build/css'));
});

gulp.task('pack-js', function () {
    return gulp.src([
        'assets/js/vendors/jquery-ui.js',
        'assets/js/iframeResizer.contentWindow.min.js',
        'assets/js/main.js',
    ])
        .pipe(concat('bundle.js'))
        .pipe(gulp.dest('public/build/js'));
});

gulp.task('make-css', gulp.series('compile-sass', 'pack-css'));

gulp.task('default', gulp.series('make-css', 'pack-js'))

gulp.task('watch', function () {
    gulp.watch('assets/scss/**/*.scss', gulp.series('make-css'));
    gulp.watch('assets/js/**/*.js', gulp.series('pack-js'));
});
