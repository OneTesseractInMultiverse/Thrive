var gulp         = require('gulp'),
    autoprefixer = require('gulp-autoprefixer'),
    concat       = require('gulp-concat'),
    connect      = require('gulp-connect'),
    cssmin       = require('gulp-cssmin'),
    header       = require('gulp-header'),
    inject       = require('gulp-inject'),
    open         = require('gulp-open'),
    plumber      = require('gulp-plumber'),
    rename       = require('gulp-rename'),
    sass         = require('gulp-ruby-sass'),
    uglify       = require('gulp-uglify'),
    browserSync  = require('browser-sync'),
    reload       = browserSync.reload;

    var pkg = require('./package.json');
    var banner = ['/**',
    ' * Bootkit v<%= pkg.version %> (<%= pkg.homepage %>)',
    ' * Copyright 2017 <%= pkg.author %>',
    ' * Licensed under the <%= pkg.license %> license',
    ' */',
    ''].join('\n');

    var helpers = ['build/js/app-nav.js',
                   'build/js/script.js',
                   'build/js/mailbox.js',
                   'build/js/note.js'];

    gulp.task('js', function(){
        gulp.src(helpers)
        .pipe(plumber())
        .pipe(concat('main.js'))
        .pipe(header(banner, { pkg : pkg } ))
        .pipe(gulp.dest('dist/js'))
        .pipe(uglify())
        .pipe(rename({suffix: '.min'}))
        .pipe(header(banner, { pkg : pkg } ))
        .pipe(gulp.dest('dist/js'))
        .pipe(connect.reload());
    });

    // sass
    gulp.task('sass', function(){
        return sass('build/sass/main.scss')
        .pipe(plumber())
        .pipe(autoprefixer({
            browsers: ['Android >= 2.1',
            'Chrome >= 21',
            'Edge >= 12',
            'Explorer >= 7',
            'Firefox >= 17',
            'Opera >= 12.1',
            'Safari >= 6.0'],
            cascade: false}))
        .pipe(header(banner, { pkg : pkg } ))
        .pipe(gulp.dest('dist/css'))
        .pipe(cssmin())
        .pipe(rename({suffix: '.min'}))
        .pipe(header(banner, { pkg : pkg } ))
        .pipe(gulp.dest('dist/css'))
        .pipe(connect.reload());;
    });

    // gulp inject
    gulp.task('inject', function(){
        var source = gulp.src([ 'bower_components/bootstrap/dist/css/bootstrap.min.css',
                                'bower_components/font-awesome/css/font-awesome.min.css',
                                'bower_components/jquery/dist/jquery.min.js',
                                'bower_components/bootstrap/dist/js/bootstrap.min.js',
                                'bower_components/jquery.nicescroll/dist/jquery.nicescroll.min.js',
                                'bower_components/autosize/dist/autosize.min.js'], {read: false});
        gulp.src('*.html')
            .pipe(inject(source, {relative: true}))
            .pipe(gulp.dest('./'))
    });

    // Connect
    gulp.task('connect', function() {
      connect.server({
        root: '.',
        port: 8080,
        livereload: true
      });
    });

    // Open target file with default application
    gulp.task('open', function(){
      var options = {
        uri: 'http://localhost:8080/'
      };
      gulp.src('.')
      .pipe(open(options));
    });

    var watchman = ['*.html'];

    gulp.task('watchman', function () {
      gulp.src(watchman)
        .pipe(connect.reload());
    });

    // Watch
    gulp.task('watch', function(){
        gulp.watch('build/js/*.js', ['js']);
        gulp.watch('build/sass/**/*.scss', ['sass']);
        gulp.watch(watchman, ['watchman']);
    });

    gulp.task('build', ['sass', 'js']);
    gulp.task('serve', ['connect', 'open', 'watch']);
    gulp.task('default', ['sass', 'js', 'connect', 'open', 'watch']);
