// Debug bullets visibility
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Debug bullets script loaded');
    
    setTimeout(function() {
        console.log('🔍 Debugging bullets visibility...');
        
        // Find all bullet containers
        const bulletContainers = document.querySelectorAll('.force-bullets, .universal-bullets, .quality-bullets');
        console.log('📊 Found bullet containers:', bulletContainers.length);
        
        bulletContainers.forEach(function(container, index) {
            console.log(`🔧 Debugging container ${index}:`);
            console.log('  - Class:', container.className);
            console.log('  - Computed display:', window.getComputedStyle(container).display);
            console.log('  - Computed visibility:', window.getComputedStyle(container).visibility);
            console.log('  - Computed opacity:', window.getComputedStyle(container).opacity);
            console.log('  - Computed position:', window.getComputedStyle(container).position);
            console.log('  - Computed z-index:', window.getComputedStyle(container).zIndex);
            console.log('  - Client rect:', container.getBoundingClientRect());
            console.log('  - Parent element:', container.parentElement);
            console.log('  - Children count:', container.children.length);
            
            // Force extreme visibility
            container.style.cssText = `
                display: block !important;
                visibility: visible !important;
                opacity: 1 !important;
                position: relative !important;
                z-index: 9999 !important;
                background: yellow !important;
                border: 2px solid red !important;
                margin-top: 16px !important;
                padding: 16px !important;
                color: #0e4580 !important;
                font-size: 0.9rem !important;
                line-height: 1.5 !important;
                border-top: 1px solid #e0e0e0 !important;
                width: 100% !important;
                box-sizing: border-box !important;
            `;
            
            // Force all children to be visible
            const bullets = container.querySelectorAll('div');
            bullets.forEach(function(bullet, bulletIndex) {
                console.log(`  - Bullet ${bulletIndex}:`, bullet.textContent);
                bullet.style.cssText = `
                    display: block !important;
                    visibility: visible !important;
                    opacity: 1 !important;
                    color: red !important;
                    background: white !important;
                    border: 1px solid blue !important;
                    margin-bottom: 8px !important;
                    padding: 4px !important;
                    font-size: 0.9rem !important;
                    font-weight: 500 !important;
                    line-height: 1.4 !important;
                    width: 100% !important;
                `;
            });
            
            console.log(`✅ Applied extreme visibility to container ${index}`);
        });
        
        // Also check if cards have proper styling
        const allCards = document.querySelectorAll('.quality-card, .advantage-card, .service-card');
        console.log('📊 Found cards:', allCards.length);
        
        allCards.forEach(function(card, index) {
            console.log(`🔧 Card ${index} styling:`);
            console.log('  - Computed height:', window.getComputedStyle(card).height);
            console.log('  - Computed overflow:', window.getComputedStyle(card).overflow);
            console.log('  - Computed position:', window.getComputedStyle(card).position);
            console.log('  - Client rect:', card.getBoundingClientRect());
            
            // Force card to be visible and have proper height
            card.style.cssText = `
                background: #ffffff !important;
                border-radius: 8px !important;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
                padding: 32px !important;
                text-align: left !important;
                width: 100% !important;
                min-height: 400px !important;
                height: auto !important;
                display: flex !important;
                flex-direction: column !important;
                position: relative !important;
                margin-bottom: 24px !important;
                overflow: visible !important;
                border: 2px solid green !important;
            `;
        });
        
        console.log('🎉 Debug bullets completed');
        
    }, 2000);
});


