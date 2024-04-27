import { viteBundler } from '@vuepress/bundler-vite'
import { defaultTheme } from '@vuepress/theme-default'
import { defineUserConfig } from 'vuepress'
import { copyCodePlugin } from '@vuepress/plugin-copy-code'
import { backToTopPlugin } from '@vuepress/plugin-back-to-top'
import { docsearchPlugin } from '@vuepress/plugin-docsearch'
import { externalLinkIconPlugin } from '@vuepress/plugin-external-link-icon'
import { gitPlugin } from '@vuepress/plugin-git'


export default defineUserConfig({
    base: '/toyllm/',
    title: 'toyllm',
    description: '',
    bundler: viteBundler(),
    theme: defaultTheme(),
    plugins: [
        // https://ecosystem.vuejs.press/zh/plugins/copy-code.html
        copyCodePlugin({
            showInMobile: true,
        }),
        // https://ecosystem.vuejs.press/zh/plugins/back-to-top.html
        backToTopPlugin(),
        // https://ecosystem.vuejs.press/zh/plugins/docsearch.html
        docsearchPlugin({
            locales: {
                '/': {
                    placeholder: '搜索文档',
                    translations: {
                        button: {
                            buttonText: '搜索文档',
                        },
                    },
                },
            }
        }),
        externalLinkIconPlugin({}),
        gitPlugin({}),
    ],
})
