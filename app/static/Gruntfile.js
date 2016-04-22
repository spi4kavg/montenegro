module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        watch: {
          scripts: {
            files: [
                'Gruntfile.js',
                'js/**/*.js',
                'sass/**/*.scss'
            ],
            tasks: ['default'],
            options: {
              debounceDelay: 250
            }
          }
        },

        compass: {
            prod: {
                options: {
                    sassDir: 'sass',
                    cssDir: 'css',
                    environment: 'production',
                    outputStyle: 'compressed'
                }
            },
            dev: {
                options: {
                    sassDir: 'sass',
                    cssDir: 'vendor/css',
                    environment: 'development',
                    outputStyle: 'expanded'
                }
            }
        },

        jshint: {
            options: {
                reporter: require('jshint-stylish')
            },
            all: [
                'js/**/*.js'
            ]
        },

        uglify: {
            options: {
                wrap: true
            },
            vendors: {
                files: {
                    'vendor/js/cabinet.min.js': [
                        'js/cabinet/api.js',
                        'js/cabinet/controller.js'
                    ],
                }
            }
        },

    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-compass');

    grunt.registerTask('default', [
        'jshint:all',
        'uglify:vendors',
        'compass:prod',
    ]);

};