"""
URL configuration for civicblogs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Simple test view for debugging
def test_view(request):
    return HttpResponse("<h1>Django is working!</h1><p>Test view successfully loaded</p>")

def debug_info(request):
    import sys
    import django
    info = f"""
    <h1>Debug Info</h1>
    <p>Django Version: {django.VERSION}</p>
    <p>Python Version: {sys.version}</p>
    <p>DEBUG: {settings.DEBUG}</p>
    <p>Database: {settings.DATABASES['default']['ENGINE']}</p>
    """
    return HttpResponse(info)


def facebook_analysis_old(request):
    html = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Facebook Post Analysis - CivicSpace</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { 
                font-family: 'Kanit', sans-serif; 
                font-weight: 300;
                font-size: 14px;
                line-height: 1.4;
            }
            .text-compact { font-size: 13px; }
            .border-l-3 { border-left-width: 3px; }
        </style>
    </head>
    <body class="bg-gradient-to-br from-slate-50 via-white to-blue-50 min-h-screen">
        <div class="container mx-auto px-6 py-6 max-w-6xl">
            <!-- Compact Header -->
            <div class="text-center mb-8">
                <div class="inline-flex items-center gap-2 mb-4">
                    <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                        <span class="text-sm text-white">📊</span>
                    </div>
                    <h1 class="text-2xl font-semibold bg-gradient-to-r from-blue-600 to-blue-700 bg-clip-text text-transparent">
                        Facebook Analytics
                    </h1>
                </div>
                <p class="text-sm text-gray-500">Professional Sentiment Analysis Dashboard</p>
            </div>


            <!-- Analysis Results -->
            <div id="analysisResult" class="grid gap-6">
                <!-- Post Info -->
                <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
                    <div class="flex items-center gap-2 mb-4">
                        <span class="text-base">📝</span>
                        <h3 class="text-base font-medium text-gray-700">Post Information</h3>
                    </div>
                    <div class="grid md:grid-cols-2 gap-4 text-sm">
                        <div>
                            <div class="text-xs font-medium text-gray-500 mb-1">ANALYZED URL</div>
                            <p class="text-gray-700 break-all text-xs font-mono bg-gray-50 p-2 rounded">facebook.com/photo?fbid=122102009768985210</p>
                        </div>
                        <div>
                            <div class="text-xs font-medium text-gray-500 mb-1">ANALYSIS TIME</div>
                            <p class="text-gray-700">Just now</p>
                        </div>
                    </div>
                </div>

                <!-- Sentiment Analysis -->
                <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
                    <div class="flex items-center gap-2 mb-4">
                        <span class="text-base">💭</span>
                        <h3 class="text-base font-medium text-gray-700">Sentiment Distribution</h3>
                    </div>
                    <div class="grid grid-cols-3 gap-4">
                        <div class="text-center p-4 bg-green-50 rounded-lg border border-green-100">
                            <div class="text-lg mb-1">😊</div>
                            <div class="text-xs font-medium text-green-700 mb-1">POSITIVE</div>
                            <p class="text-lg font-semibold text-green-600">45%</p>
                        </div>
                        <div class="text-center p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <div class="text-lg mb-1">😐</div>
                            <div class="text-xs font-medium text-gray-700 mb-1">NEUTRAL</div>
                            <p class="text-lg font-semibold text-gray-600">35%</p>
                        </div>
                        <div class="text-center p-4 bg-red-50 rounded-lg border border-red-100">
                            <div class="text-lg mb-1">😞</div>
                            <div class="text-xs font-medium text-red-700 mb-1">NEGATIVE</div>
                            <p class="text-lg font-semibold text-red-600">20%</p>
                        </div>
                    </div>
                </div>

                <!-- Sample Comments -->
                <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center gap-2">
                            <span class="text-base">💬</span>
                            <h3 class="text-base font-medium text-gray-700">Sample Comments</h3>
                        </div>
                        <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">10 comments analyzed</span>
                    </div>
                    <div class="space-y-3">
                        <div class="border-l-3 border-green-400 pl-3 py-2 bg-green-50 rounded-r">
                            <p class="text-sm text-gray-700 mb-1">"เนื้อหาดีมาก ให้ความรู้เยอะ 👍"</p>
                            <span class="text-xs text-green-600 font-medium">Positive (0.85)</span>
                        </div>
                        <div class="border-l-3 border-gray-400 pl-3 py-2 bg-gray-50 rounded-r">
                            <p class="text-sm text-gray-700 mb-1">"อยากทราบรายละเอียดเพิ่มเติมครับ 🤔"</p>
                            <span class="text-xs text-gray-600 font-medium">Neutral (0.12)</span>
                        </div>
                        <div class="border-l-3 border-red-400 pl-3 py-2 bg-red-50 rounded-r">
                            <p class="text-sm text-gray-700 mb-1">"ไม่เห็นด้วยกับเรื่องนี้เลย"</p>
                            <span class="text-xs text-red-600 font-medium">Negative (-0.65)</span>
                        </div>
                    </div>
                </div>

                <!-- Charts Grid -->
                <div class="grid md:grid-cols-2 gap-4">
                    <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                        <div class="flex items-center gap-2 mb-3">
                            <span class="text-sm">📊</span>
                            <h4 class="text-sm font-medium text-gray-700">Sentiment Chart</h4>
                        </div>
                        <canvas id="sentimentChart" width="250" height="200"></canvas>
                    </div>
                    <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                        <div class="flex items-center gap-2 mb-3">
                            <span class="text-sm">📈</span>
                            <h4 class="text-sm font-medium text-gray-700">Engagement Timeline</h4>
                        </div>
                        <canvas id="timelineChart" width="250" height="200"></canvas>
                    </div>
                </div>

                <!-- Compact Summary -->
                <div class="bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl p-5 text-white">
                    <div class="flex items-center gap-2 mb-4">
                        <span class="text-base">🔍</span>
                        <h3 class="text-base font-medium">Analysis Summary</h3>
                    </div>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                            <div class="text-xs opacity-75 mb-1">ENGAGEMENT</div>
                            <p class="font-semibold">8.5%</p>
                        </div>
                        <div>
                            <div class="text-xs opacity-75 mb-1">SENTIMENT</div>
                            <p class="font-semibold">Positive</p>
                        </div>
                        <div>
                            <div class="text-xs opacity-75 mb-1">COMMENTS</div>
                            <p class="font-semibold">10 analyzed</p>
                        </div>
                        <div>
                            <div class="text-xs opacity-75 mb-1">ACCURACY</div>
                            <p class="font-semibold">94.2%</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Compact Navigation -->
            <div class="text-center mt-8">
                <a href="/" class="inline-flex items-center gap-2 bg-gray-500 text-white px-4 py-2 text-sm rounded-lg hover:bg-gray-600 transition-colors">
                    ← Back to Home
                </a>
            </div>
        </div>

        <script>
        // Global chart variables
        let sentimentChart;
        let timelineChart;
        
        // Sample Chart Implementation
        document.addEventListener('DOMContentLoaded', function() {
            // Sentiment Pie Chart
            const sentimentCtx = document.getElementById('sentimentChart').getContext('2d');
            sentimentChart = new Chart(sentimentCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Positive', 'Neutral', 'Negative'],
                    datasets: [{
                        data: [45, 35, 20],
                        backgroundColor: ['#22c55e', '#6b7280', '#ef4444']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });

            // Timeline Chart
            const timelineCtx = document.getElementById('timelineChart').getContext('2d');
            timelineChart = new Chart(timelineCtx, {
                type: 'line',
                data: {
                    labels: ['6:00', '12:00', '18:00', '24:00'],
                    datasets: [{
                        label: 'Comments per hour',
                        data: [12, 25, 18, 8],
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)'
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Form Handler with Real API Call
            document.getElementById('analyzeForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const url = document.getElementById('fbUrl').value;
                
                if (!url) {
                    alert('กรุณาป้อน URL ของโพสต์ Facebook');
                    return;
                }
                
                // Show loading
                const submitBtn = e.target.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '🔄 กำลังวิเคราะห์...';
                submitBtn.disabled = true;
                
                try {
                    const response = await fetch('/api/analyze-facebook/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            post_url: url,
                            comments: [] // Will use sample data from backend
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        updateAnalysisResults(result.data);
                        alert('✅ วิเคราะห์เสร็จแล้ว! ดูผลลัพธ์ด้านล่าง');
                    } else {
                        alert('❌ เกิดข้อผิดพลาด: ' + (result.error || 'ไม่ทราบสาเหตุ'));
                    }
                } catch (error) {
                    console.error('Analysis error:', error);
                    alert('❌ เกิดข้อผิดพลาดในการเชื่อมต่อ: ' + error.message + 
                          '\\n\\n💡 ลองรีเฟรชหน้าและทำใหม่อีกครั้ง');
                } finally {
                    // Reset button
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            });
            
            function updateAnalysisResults(data) {
                // Update URL in post info
                document.querySelector('#analysisResult .break-all').textContent = data.post_url;
                
                // Update sentiment percentages
                const analysis = data.comments_analysis;
                const percentages = analysis.sentiment_percentages;
                
                // Update sentiment cards
                const cards = document.querySelectorAll('#analysisResult .text-center');
                cards[0].querySelector('.text-2xl').textContent = percentages.positive + '%';
                cards[1].querySelector('.text-2xl').textContent = percentages.neutral + '%';
                cards[2].querySelector('.text-2xl').textContent = percentages.negative + '%';
                
                // Update sample comments with real analysis
                updateCommentsSection(analysis.individual_results.slice(0, 3));
                
                // Update charts
                updateCharts(percentages);
                
                // Update insights
                updateInsights(analysis);
                
                // Show recommendations
                showRecommendations(data.recommendations);
            }
            
            function updateCommentsSection(comments) {
                const commentsContainer = document.querySelector('#analysisResult .space-y-4');
                commentsContainer.innerHTML = '';
                
                comments.forEach(comment => {
                    const sentiment = comment.sentiment;
                    const score = comment.score;
                    const text = comment.original_text;
                    
                    let borderColor, bgColor, textColor;
                    if (sentiment === 'positive') {
                        borderColor = 'border-green-500';
                        bgColor = 'bg-green-50';
                        textColor = 'text-green-600';
                    } else if (sentiment === 'negative') {
                        borderColor = 'border-red-500';
                        bgColor = 'bg-red-50';
                        textColor = 'text-red-600';
                    } else {
                        borderColor = 'border-gray-500';
                        bgColor = 'bg-gray-50';
                        textColor = 'text-gray-600';
                    }
                    
                    const commentDiv = document.createElement('div');
                    commentDiv.className = `border-l-4 ${borderColor} pl-4 py-2 ${bgColor}`;
                    commentDiv.innerHTML = `
                        <p class="text-gray-700">"${text}"</p>
                        <span class="text-sm ${textColor} font-medium">Sentiment: ${sentiment.charAt(0).toUpperCase() + sentiment.slice(1)} (${score})</span>
                    `;
                    commentsContainer.appendChild(commentDiv);
                });
            }
            
            function updateCharts(percentages) {
                // Update sentiment chart safely
                if (sentimentChart && sentimentChart.data && sentimentChart.data.datasets && sentimentChart.data.datasets[0]) {
                    sentimentChart.data.datasets[0].data = [percentages.positive, percentages.neutral, percentages.negative];
                    sentimentChart.update();
                }
                
                // Update timeline chart with sample engagement data
                if (timelineChart && timelineChart.data && timelineChart.data.datasets && timelineChart.data.datasets[0]) {
                    // Generate sample hourly engagement based on sentiment
                    const baseEngagement = Math.floor(percentages.positive / 10);
                    timelineChart.data.datasets[0].data = [
                        baseEngagement + Math.floor(Math.random() * 5),
                        baseEngagement + Math.floor(Math.random() * 8) + 5,
                        baseEngagement + Math.floor(Math.random() * 6) + 2,
                        baseEngagement + Math.floor(Math.random() * 3)
                    ];
                    timelineChart.update();
                }
            }
            
            function updateInsights(analysis) {
                const insights = document.querySelectorAll('.text-blue-100');
                insights[0].textContent = `อัตราการมีส่วนร่วม: ${((analysis.total_comments / 1000) * 100).toFixed(1)}%`;
                insights[1].textContent = `โดยรวม: ${analysis.average_score > 0 ? 'ทางบวก (Positive)' : analysis.average_score < 0 ? 'ทางลบ (Negative)' : 'เป็นกลาง (Neutral)'}`;
                insights[2].textContent = `ความคิดเห็นทั้งหมด: ${analysis.total_comments} ข้อ`;
                insights[3].textContent = `คะแนนเฉลี่ย: ${analysis.average_score}`;
            }
            
            function showRecommendations(recommendations) {
                if (recommendations && recommendations.length > 0) {
                    alert('💡 คำแนะนำ:\\n\\n' + recommendations.join('\\n'));
                }
            }
        });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)

def simple_homepage(request):
    html = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>CivicSpace - แพลตฟอร์มสื่อสารสาธารณะ</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Kanit', sans-serif; }
        </style>
    </head>
    <body class="bg-gradient-to-br from-yellow-50 via-white to-yellow-100 min-h-screen">
        <!-- Hero Section -->
        <div class="container mx-auto px-4 py-16">
            <div class="text-center mb-16">
                <div class="inline-flex items-center gap-3 mb-6">
                    <div class="w-16 h-16 bg-gradient-to-r from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center">
                        <span class="text-2xl">🎥</span>
                    </div>
                    <h1 class="text-5xl font-bold bg-gradient-to-r from-yellow-600 to-yellow-800 bg-clip-text text-transparent">
                        CivicSpace
                    </h1>
                </div>
                <p class="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
                    แพลตฟอร์มสื่อสารสาธารณะ สำหรับแบ่งปันเรื่องราวและวิดีโอ เพื่อสร้างการมีส่วนร่วมในสังคม
                </p>
            </div>

            <!-- API Statistics -->
            <div class="grid md:grid-cols-3 gap-8 mb-16">
                <div class="bg-white rounded-2xl p-8 shadow-lg border border-yellow-100">
                    <div class="text-3xl mb-4">📹</div>
                    <h3 class="text-2xl font-semibold text-gray-800 mb-2">Video API</h3>
                    <p class="text-gray-600">ระบบจัดการวิดีโอครบครัน พร้อม analytics และ search</p>
                </div>
                <div class="bg-white rounded-2xl p-8 shadow-lg border border-yellow-100">
                    <div class="text-3xl mb-4">📝</div>
                    <h3 class="text-2xl font-semibold text-gray-800 mb-2">Blog System</h3>
                    <p class="text-gray-600">ระบบบล็อกพร้อม CKEditor และระบบ tagging</p>
                </div>
                <div class="bg-white rounded-2xl p-8 shadow-lg border border-yellow-100">
                    <div class="text-3xl mb-4">🔗</div>
                    <h3 class="text-2xl font-semibold text-gray-800 mb-2">REST API</h3>
                    <p class="text-gray-600">API สำหรับ Next.js พร้อม CORS และ pagination</p>
                </div>
            </div>

            <!-- API Endpoints -->
            <div class="bg-white rounded-2xl p-8 shadow-lg border border-yellow-100 mb-12">
                <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">🚀 API Endpoints</h2>
                <div class="grid md:grid-cols-2 gap-6">
                    <div class="space-y-4">
                        <h3 class="text-xl font-semibold text-yellow-700 border-b border-yellow-200 pb-2">📹 Video API</h3>
                        <div class="space-y-2">
                            <a href="/api/v1/videos/" class="block p-3 rounded-lg bg-yellow-50 hover:bg-yellow-100 transition-colors">
                                <code class="text-yellow-700">/api/v1/videos/</code>
                                <span class="text-gray-600 ml-2">รายการวิดีโอทั้งหมด</span>
                            </a>
                            <a href="/api/v1/videos/latest/" class="block p-3 rounded-lg bg-yellow-50 hover:bg-yellow-100 transition-colors">
                                <code class="text-yellow-700">/api/v1/videos/latest/</code>
                                <span class="text-gray-600 ml-2">วิดีโอล่าสุด</span>
                            </a>
                            <a href="/api/v1/videos/popular/" class="block p-3 rounded-lg bg-yellow-50 hover:bg-yellow-100 transition-colors">
                                <code class="text-yellow-700">/api/v1/videos/popular/</code>
                                <span class="text-gray-600 ml-2">วิดีโอยอดนิยม</span>
                            </a>
                        </div>
                    </div>
                    <div class="space-y-4">
                        <h3 class="text-xl font-semibold text-yellow-700 border-b border-yellow-200 pb-2">📝 Content API</h3>
                        <div class="space-y-2">
                            <a href="/api/v1/posts/" class="block p-3 rounded-lg bg-yellow-50 hover:bg-yellow-100 transition-colors">
                                <code class="text-yellow-700">/api/v1/posts/</code>
                                <span class="text-gray-600 ml-2">รายการบทความ</span>
                            </a>
                            <a href="/api/v1/categories/" class="block p-3 rounded-lg bg-yellow-50 hover:bg-yellow-100 transition-colors">
                                <code class="text-yellow-700">/api/v1/categories/</code>
                                <span class="text-gray-600 ml-2">หมวดหมู่</span>
                            </a>
                            <a href="/api/v1/tags/" class="block p-3 rounded-lg bg-yellow-50 hover:bg-yellow-100 transition-colors">
                                <code class="text-yellow-700">/api/v1/tags/</code>
                                <span class="text-gray-600 ml-2">แท็ก</span>
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Features -->
            <div class="bg-gradient-to-r from-yellow-400 to-yellow-600 rounded-2xl p-8 text-white mb-12">
                <h2 class="text-3xl font-bold mb-8 text-center">✨ คุณสมบัติเด่น</h2>
                <div class="grid md:grid-cols-2 gap-8">
                    <div class="space-y-4">
                        <div class="flex items-start gap-3">
                            <span class="text-xl">🔍</span>
                            <div>
                                <h4 class="font-semibold">ระบบค้นหาข้อมูล</h4>
                                <p class="text-yellow-100">ค้นหาในเนื้อหา ชื่อเรื่อง และหมวดหมู่</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-3">
                            <span class="text-xl">📊</span>
                            <div>
                                <h4 class="font-semibold">Analytics & Metrics</h4>
                                <p class="text-yellow-100">ติดตามยอดเข้าชมและสถิติการใช้งาน</p>
                            </div>
                        </div>
                    </div>
                    <div class="space-y-4">
                        <div class="flex items-start gap-3">
                            <span class="text-xl">📱</span>
                            <div>
                                <h4 class="font-semibold">Responsive Design</h4>
                                <p class="text-yellow-100">รองรับทุกขนาดหน้าจอ Mobile-first</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-3">
                            <span class="text-xl">☁️</span>
                            <div>
                                <h4 class="font-semibold">Azure Cloud Storage</h4>
                                <p class="text-yellow-100">จัดเก็บไฟล์มีเดียบน Azure Blob Storage</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tools & Analysis -->
            <div class="bg-white rounded-2xl p-8 shadow-lg border border-yellow-100 mb-12">
                <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">🛠️ เครื่องมือวิเคราะห์</h2>
                <div class="grid md:grid-cols-3 gap-6">
                    <a href="/facebook/" class="block p-6 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all transform hover:scale-105">
                        <div class="text-3xl mb-3">📊</div>
                        <h3 class="text-xl font-semibold mb-2">Facebook Analysis</h3>
                        <p class="text-blue-100">วิเคราะห์โพสต์และ sentiment</p>
                    </a>
                    <a href="/admin/" class="block p-6 bg-gradient-to-r from-gray-700 to-gray-800 text-white rounded-xl hover:from-gray-800 hover:to-gray-900 transition-all transform hover:scale-105">
                        <div class="text-3xl mb-3">⚙️</div>
                        <h3 class="text-xl font-semibold mb-2">Admin Panel</h3>
                        <p class="text-gray-300">จัดการเนื้อหาและข้อมูล</p>
                    </a>
                    <a href="/debug/" class="block p-6 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 transition-all transform hover:scale-105">
                        <div class="text-3xl mb-3">🔧</div>
                        <h3 class="text-xl font-semibold mb-2">Debug Info</h3>
                        <p class="text-green-100">ข้อมูลระบบและการตั้งค่า</p>
                    </a>
                </div>
            </div>

            <!-- Footer -->
            <div class="text-center mt-16 text-gray-500">
                <p>Built with Django 5.2.5 • PostgreSQL • Azure Cloud • Next.js Ready</p>
                <p class="mt-2">🤖 Generated with <a href="https://claude.ai/code" class="text-yellow-600 hover:underline">Claude Code</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/', include('blog.api_urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    # Debug URLs
    path('test/', test_view, name='test'),
    path('debug/', debug_info, name='debug'),
    # Temporary simple homepage to bypass blog view errors
    path('', simple_homepage, name='homepage'),
    # Blog URLs (temporarily disabled due to production 500 errors)
    path('blog/', include('blog.urls')),
]

# Serve media files in both development and production
# Note: For production, consider using Azure Blob Storage for better performance
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
