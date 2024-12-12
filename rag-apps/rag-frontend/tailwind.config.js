/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{js,ts,jsx,tsx}', './node_modules/@centml/ui/dist/**/*.js'],
	darkMode: 'selector',
	theme: {
		extend: {
			colors: {
				primary: {
					50: 'rgb(217, 242, 235)',
					100: 'rgb(204, 238, 229)',
					200: 'rgb(191, 233, 222)',
					300: 'rgb(153, 220, 202)',
					400: 'rgb(77, 194, 163)',
					500: 'rgb(0, 168, 123)',
					600: 'rgb(0, 151, 111)',
					700: 'rgb(0, 126, 92)',
					800: 'rgb(0, 101, 74)',
					900: 'rgb(0, 82, 60)'
				},
				secondary: {
					50: 'rgb(217, 227, 224)',
					100: 'rgb(204, 217, 214)',
					200: 'rgb(191, 208, 204)',
					300: 'rgb(153, 180, 173)',
					400: 'rgb(77, 123, 111)',
					500: 'rgb(0, 67, 49)',
					600: 'rgb(0, 60, 44)',
					700: 'rgb(0, 50, 37)',
					800: 'rgb(0, 40, 29)',
					900: 'rgb(0, 33, 24)'
				},
				tertiary: {
					50: 'rgb(255, 239, 217)',
					100: 'rgb(255, 234, 204)',
					200: 'rgb(255, 229, 191)',
					300: 'rgb(255, 213, 153)',
					400: 'rgb(255, 181, 77)',
					500: 'rgb(255, 149, 0)',
					600: 'rgb(230, 134, 0)',
					700: 'rgb(191, 112, 0)',
					800: 'rgb(153, 89, 0)',
					900: 'rgb(125, 73, 0)'
				},
				success: {
					50: 'rgb(225, 247, 230)',
					100: 'rgb(214, 244, 222)',
					200: 'rgb(204, 241, 214)',
					300: 'rgb(174, 233, 189)',
					400: 'rgb(113, 216, 139)',
					500: 'rgb(52, 199, 89)',
					600: 'rgb(47, 179, 80)',
					700: 'rgb(39, 149, 67)',
					800: 'rgb(31, 119, 53)',
					900: 'rgb(25, 98, 44)'
				},
				warning: {
					50: 'rgb(255 247 217)',
					100: 'rgb( 255 245 204)',
					200: 'rgb( 255 242 191)',
					300: 'rgb( 255 235 153)',
					400: 'rgb( 255 219 77)',
					500: 'rgb( 255 204 0)',
					600: 'rgb( 230 184 0)',
					700: 'rgb( 191 153 0)',
					800: 'rgb( 153 122 0)',
					900: 'rgb( 125 100 0)'
				},
				error: {
					50: 'rgb(251, 224, 224)',
					100: 'rgb(249, 214, 214)',
					200: 'rgb(248, 204, 204)',
					300: 'rgb(243, 173, 173)',
					400: 'rgb(234, 112, 112)',
					500: 'rgb(225, 51, 51)',
					600: 'rgb(203, 46, 46)',
					700: 'rgb(169, 38, 38)',
					800: 'rgb(135, 31, 31)',
					900: 'rgb(110, 25, 25)'
				}
			}
		}
	},
	plugins: []
};
