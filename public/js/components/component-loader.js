/**
 * コンポーネントローダー
 * HTMLファイルから共通コンポーネントを動的に読み込む
 */

class ComponentLoader {
    constructor() {
        this.cache = new Map();
        // 現在のスクリプトの場所を基準にした相対パスを設定
        this.basePath = this.getBasePath();
    }
    
    getBasePath() {
        // 現在実行中のスクリプトの場所を取得
        const currentScript = document.currentScript;
        if (currentScript && currentScript.src) {
            const scriptPath = currentScript.src;
            // component-loader.jsからviews/components/への相対パス
            return '../views/components/';
        }
        
        // フォールバック: URLベースの判定
        const currentPath = window.location.pathname || window.location.href;
        
        if (currentPath.includes('views/products/') || currentPath.includes('/products/')) {
            return '../../../../../iei/ieir/views/components/';
        } else if (currentPath.includes('views/categories/') || currentPath.includes('/categories/')) {
            return '../../../../iei/ieir/views/components/';
        } else {
            // デフォルト
            return '../views/components/';
        }
    }

    /**
     * コンポーネントを読み込んで指定された要素に挿入
     * @param {string} componentName - コンポーネント名
     * @param {string} targetSelector - 挿入先のセレクタ
     * @param {boolean} useCache - キャッシュを使用するか
     */
    async load(componentName, targetSelector, useCache = true) {
        try {
            let html;
            
            if (useCache && this.cache.has(componentName)) {
                html = this.cache.get(componentName);
            } else {
                const componentUrl = `${this.basePath}${componentName}.html`;
                console.log(`Loading component: ${componentName} from ${componentUrl}`);
                
                const response = await fetch(componentUrl);
                if (!response.ok) {
                    throw new Error(`コンポーネント "${componentName}" の読み込みに失敗しました: ${response.status} (URL: ${componentUrl})`);
                }
                
                html = await response.text();
                
                if (useCache) {
                    this.cache.set(componentName, html);
                }
            }
            
            const targetElement = document.querySelector(targetSelector);
            if (!targetElement) {
                throw new Error(`ターゲット要素 "${targetSelector}" が見つかりません`);
            }
            
            targetElement.innerHTML = html;
            
            // スクリプトタグを実行
            this.executeScripts(targetElement);
            
            console.log(`コンポーネント "${componentName}" を "${targetSelector}" に読み込みました`);
            
        } catch (error) {
            console.error('コンポーネントの読み込みエラー:', error);
            
            // エラー時のフォールバック表示
            const targetElement = document.querySelector(targetSelector);
            if (targetElement) {
                targetElement.innerHTML = `
                    <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
                        <p class="text-sm">コンポーネントの読み込みに失敗しました: ${componentName}</p>
                    </div>
                `;
            }
        }
    }

    /**
     * 複数のコンポーネントを同時に読み込み
     * @param {Array} components - [{name: 'header', target: '#header'}, ...]
     */
    async loadMultiple(components) {
        const promises = components.map(component => 
            this.load(component.name, component.target, component.cache !== false)
        );
        
        await Promise.all(promises);
    }

    /**
     * 読み込んだHTMLに含まれるscriptタグを実行
     * @param {Element} container - コンテナ要素
     */
    executeScripts(container) {
        const scripts = container.querySelectorAll('script');
        scripts.forEach(script => {
            const newScript = document.createElement('script');
            
            if (script.src) {
                newScript.src = script.src;
            } else {
                newScript.textContent = script.textContent;
            }
            
            // 元のscriptの属性をコピー
            Array.from(script.attributes).forEach(attr => {
                if (attr.name !== 'src' && attr.name !== 'type') {
                    newScript.setAttribute(attr.name, attr.value);
                }
            });
            
            document.head.appendChild(newScript);
            script.remove();
        });
    }

    /**
     * キャッシュをクリア
     * @param {string} componentName - 特定のコンポーネント名（省略時は全てクリア）
     */
    clearCache(componentName = null) {
        if (componentName) {
            this.cache.delete(componentName);
        } else {
            this.cache.clear();
        }
    }

    /**
     * プリロード：事前にコンポーネントをキャッシュに読み込み
     * @param {Array} componentNames - コンポーネント名の配列
     */
    async preload(componentNames) {
        const promises = componentNames.map(async (name) => {
            try {
                const response = await fetch(`${this.basePath}${name}.html`);
                if (response.ok) {
                    const html = await response.text();
                    this.cache.set(name, html);
                    console.log(`コンポーネント "${name}" をプリロードしました`);
                }
            } catch (error) {
                console.warn(`コンポーネント "${name}" のプリロードに失敗:`, error);
            }
        });
        
        await Promise.all(promises);
    }
}

// グローバルインスタンス作成
window.componentLoader = new ComponentLoader();

// jQuery拡張（jQueryが利用可能な場合）
if (window.jQuery) {
    jQuery.fn.loadComponent = function(componentName, useCache = true) {
        const targetSelector = `#${this.attr('id')}` || this.get(0);
        return window.componentLoader.load(componentName, targetSelector, useCache);
    };
}

// 便利関数
window.loadComponent = (name, target, cache = true) => {
    return window.componentLoader.load(name, target, cache);
};

window.loadComponents = (components) => {
    return window.componentLoader.loadMultiple(components);
};

// DOM読み込み完了後の自動処理
document.addEventListener('DOMContentLoaded', () => {
    // data-component属性を持つ要素を自動的に処理
    const autoLoadElements = document.querySelectorAll('[data-component]');
    
    autoLoadElements.forEach(element => {
        const componentName = element.getAttribute('data-component');
        const targetSelector = `#${element.id}` || element;
        
        if (componentName) {
            window.componentLoader.load(componentName, targetSelector);
        }
    });
    
    // 一般的なコンポーネントのプリロード
    const commonComponents = ['header', 'footer'];
    window.componentLoader.preload(commonComponents);
});

// エクスポート（ES6モジュール対応）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ComponentLoader;
}