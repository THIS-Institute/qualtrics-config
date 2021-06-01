'use strict';

var gulp = require('gulp');
var concat = require('gulp-concat')
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');

gulp.task('compile-sass', function () {
    return gulp.src('scss/main.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(autoprefixer({
            overrideBrowserslist: ['last 10 versions'],
            cascade: false
        }))
        .pipe(gulp.dest('css'));
});

gulp.task('pack-css', function () {
    return gulp.src([
        'jquery-ui-1.12.1.custom/jquery-ui.css',
        'jquery-ui-1.12.1.custom/jquery-ui.structure.css',
        'jquery-ui-1.12.1.custom/jquery-ui.theme.css',
        'css/main.css',
    ])
        .pipe(concat('bundle.css'))
        .pipe(gulp.dest('public/build/css'));
});

gulp.task('default', gulp.series('compile-sass', 'pack-css'));

gulp.task('watch', function () {
    gulp.watch('./scss/**/*.scss', gulp.series('default'));
});