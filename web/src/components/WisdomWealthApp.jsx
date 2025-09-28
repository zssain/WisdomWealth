import React, { useState, useRef } from 'react';

const WisdomWealthApp = () => {
  const [currentPage, setCurrentPage] = useState('home');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  // Professional service cards with fintech styling
  const serviceCards = [
    {
      icon: 'fas fa-shield-alt',
      title: 'Fraud Protection',
      description: 'Advanced threat detection and real-time security monitoring',
      color: 'var(--primary-brand)',
      bgColor: '#f0f4f8'
    },
    {
      icon: 'fas fa-heartbeat',
      title: 'Healthcare Finance',
      description: 'Medical billing optimization and insurance management',
      color: 'var(--accent-color)',
      bgColor: '#ecfeff'
    },
    {
      icon: 'fas fa-file-contract',
      title: 'Estate Planning',
      description: 'Document management and succession planning',
      color: 'var(--success-color)',
      bgColor: '#f0fdf4'
    },
    {
      icon: 'fas fa-users-cog',
      title: 'Family Coordination',
      description: 'Secure communication and emergency protocols',
      color: 'var(--warning-color)',
      bgColor: '#fffbeb'
    }
  ];

  // Modern Professional Navigation
  const Navigation = () => (
    <nav style={{
      background: 'white',
      borderBottom: '1px solid var(--gray-200)',
      position: 'sticky',
      top: 0,
      zIndex: 1000,
      boxShadow: 'var(--shadow-sm)'
    }}>
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0 var(--space-6)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
          <div style={{
            width: '32px',
            height: '32px',
            background: 'linear-gradient(135deg, var(--primary-brand), var(--primary-light))',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <i className="fas fa-shield-alt" style={{ fontSize: '16px', color: 'white' }}></i>
          </div>
          <span style={{
            fontSize: 'var(--text-xl)',
            fontWeight: '600',
            color: 'var(--gray-900)'
          }}>
            WisdomWealth
          </span>
        </div>

        <div style={{
          display: 'flex',
          background: 'var(--gray-100)',
          borderRadius: 'var(--radius-lg)',
          padding: 'var(--space-1)'
        }}>
          {[
            { id: 'home', label: 'Home', icon: 'fas fa-home' },
            { id: 'chat', label: 'Security Assistant', icon: 'fas fa-comments' },
            { id: 'upload', label: 'Documents', icon: 'fas fa-upload' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setCurrentPage(tab.id)}
              style={{
                background: currentPage === tab.id ? 'white' : 'transparent',
                color: currentPage === tab.id ? 'var(--primary-brand)' : 'var(--gray-600)',
                border: 'none',
                padding: 'var(--space-2) var(--space-4)',
                borderRadius: 'var(--radius-md)',
                fontSize: 'var(--text-sm)',
                fontWeight: '500',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--space-2)',
                boxShadow: currentPage === tab.id ? 'var(--shadow-sm)' : 'none'
              }}
            >
              <i className={tab.icon} style={{ fontSize: '14px' }}></i>
              {tab.label}
            </button>
          ))}
        </div>
      </div>
    </nav>
  );

  // Professional Homepage
  const HomePage = () => (
    <div style={{
      minHeight: 'calc(100vh - 72px)',
      background: 'linear-gradient(135deg, var(--gray-50) 0%, white 100%)'
    }}>
      {/* Hero Section */}
      <section style={{
        padding: 'var(--space-16) var(--space-6) var(--space-12)',
        textAlign: 'center',
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        <div style={{
          width: '80px',
          height: '80px',
          background: 'linear-gradient(135deg, var(--primary-brand), var(--primary-light))',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto var(--space-6)',
          boxShadow: 'var(--shadow-lg)'
        }}>
          <i className="fas fa-shield-alt" style={{ fontSize: '32px', color: 'white' }}></i>
        </div>

        <h1 style={{
          fontSize: 'clamp(2.5rem, 5vw, 3.5rem)',
          fontWeight: '700',
          color: 'var(--gray-900)',
          marginBottom: 'var(--space-4)',
          lineHeight: '1.1'
        }}>
          Financial Security Platform for Seniors
        </h1>

        <p style={{
          fontSize: 'var(--text-xl)',
          color: 'var(--gray-600)',
          marginBottom: 'var(--space-8)',
          maxWidth: '600px',
          margin: '0 auto var(--space-8)',
          lineHeight: '1.6'
        }}>
          Comprehensive protection against fraud, healthcare billing support, 
          and family coordination with AI-powered security assistance.
        </p>

        <div style={{
          display: 'flex',
          gap: 'var(--space-4)',
          justifyContent: 'center',
          flexWrap: 'wrap'
        }}>
          <button
            onClick={() => setCurrentPage('chat')}
            style={{
              background: 'var(--primary-brand)',
              color: 'white',
              border: 'none',
              padding: 'var(--space-3) var(--space-6)',
              borderRadius: 'var(--radius-lg)',
              fontSize: 'var(--text-lg)',
              fontWeight: '600',
              cursor: 'pointer',
              boxShadow: 'var(--shadow-md)',
              transition: 'all 0.2s ease',
              display: 'flex',
              alignItems: 'center',
              gap: 'var(--space-2)'
            }}
          >
            <i className="fas fa-comments"></i>
            Start Security Chat
          </button>

          <button
            onClick={() => setCurrentPage('upload')}
            style={{
              background: 'white',
              color: 'var(--primary-brand)',
              border: '2px solid var(--primary-brand)',
              padding: 'var(--space-3) var(--space-6)',
              borderRadius: 'var(--radius-lg)',
              fontSize: 'var(--text-lg)',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              display: 'flex',
              alignItems: 'center',
              gap: 'var(--space-2)'
            }}
          >
            <i className="fas fa-upload"></i>
            Upload Documents
          </button>
        </div>
      </section>

      {/* Services Grid */}
      <section style={{
        padding: 'var(--space-12) var(--space-6)',
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        <div style={{
          textAlign: 'center',
          marginBottom: 'var(--space-12)'
        }}>
          <h2 style={{
            fontSize: 'var(--text-3xl)',
            fontWeight: '600',
            color: 'var(--gray-900)',
            marginBottom: 'var(--space-3)'
          }}>
            Comprehensive Security Services
          </h2>
          <p style={{
            fontSize: 'var(--text-lg)',
            color: 'var(--gray-600)',
            maxWidth: '600px',
            margin: '0 auto'
          }}>
            Advanced AI protection tailored specifically for senior financial security
          </p>
        </div>

        <div className="grid grid-cols-2" style={{
          gap: 'var(--space-6)'
        }}>
          {serviceCards.map((service, index) => (
            <div
              key={index}
              className="card"
              style={{
                background: service.bgColor,
                border: '1px solid var(--gray-200)',
                borderRadius: 'var(--radius-xl)',
                padding: 'var(--space-8)',
                textAlign: 'center',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                position: 'relative',
                overflow: 'hidden'
              }}
              onClick={() => setCurrentPage('chat')}
            >
              <div style={{
                width: '64px',
                height: '64px',
                background: service.color,
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto var(--space-4)',
                boxShadow: 'var(--shadow-lg)'
              }}>
                <i className={service.icon} style={{ fontSize: '24px', color: 'white' }}></i>
              </div>

              <h3 style={{
                fontSize: 'var(--text-xl)',
                fontWeight: '600',
                color: 'var(--gray-900)',
                marginBottom: 'var(--space-2)'
              }}>
                {service.title}
              </h3>

              <p style={{
                fontSize: 'var(--text-base)',
                color: 'var(--gray-600)',
                lineHeight: '1.5',
                marginBottom: 'var(--space-4)'
              }}>
                {service.description}
              </p>

              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 'var(--space-2)',
                color: service.color,
                fontWeight: '600',
                fontSize: 'var(--text-sm)'
              }}>
                Learn More
                <i className="fas fa-arrow-right" style={{ fontSize: '12px' }}></i>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );

  // Modern Chat Interface
  const ChatPage = () => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    React.useEffect(() => {
      scrollToBottom();
    }, [messages]);

    const handleSendMessage = async () => {
      if (!inputMessage.trim()) return;

      const userMessage = {
        id: Date.now(),
        type: 'user',
        text: inputMessage,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, userMessage]);
      setInputMessage('');
      setIsTyping(true);

      try {
        // Use environment variable or fallback to localhost for development
        const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const response = await fetch(`${API_URL}/route`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: `user_${Date.now()}`,
            text: inputMessage,
            meta: { timestamp: new Date().toISOString() }
          })
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        
        const botMessage = {
          id: Date.now() + 1,
          type: 'agent',
          text: data.response || 'I received your message and I\'m here to help with your financial security.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          risk: data.risk_level,
          agent_type: data.agent_type,
          confidence: data.confidence_score
        };

        setMessages(prev => [...prev, botMessage]);
      } catch (error) {
        console.error('Error sending message:', error);
        const errorMessage = {
          id: Date.now() + 1,
          type: 'error',
          text: 'Connection issue - please try again in a moment.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, errorMessage]);
      } finally {
        setIsTyping(false);
      }
    };

    const handleKeyPress = (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSendMessage();
      }
    };

    return (
      <div style={{
        height: 'calc(100vh - 72px)',
        background: 'var(--gray-50)',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {/* Modern Chat Header */}
        <div style={{
          background: 'white',
          borderBottom: '1px solid var(--gray-200)',
          padding: 'var(--space-4) var(--space-6)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-3)'
          }}>
            <div style={{
              width: '40px',
              height: '40px',
              background: 'var(--primary-brand)',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <i className="fas fa-robot" style={{ fontSize: '20px', color: 'white' }}></i>
            </div>
            <div>
              <h2 style={{
                margin: 0,
                fontSize: 'var(--text-lg)',
                fontWeight: '600',
                color: 'var(--gray-900)'
              }}>
                WisdomWealth Security AI
              </h2>
              <p style={{
                margin: 0,
                fontSize: 'var(--text-sm)',
                color: 'var(--gray-500)'
              }}>
                Financial Protection Assistant
              </p>
            </div>
          </div>
          
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-2)',
            padding: 'var(--space-2) var(--space-3)',
            background: 'var(--gray-50)',
            borderRadius: 'var(--radius-lg)',
            border: '1px solid var(--gray-200)'
          }}>
            <div style={{
              width: '8px',
              height: '8px',
              background: 'var(--success-color)',
              borderRadius: '50%'
            }}></div>
            <span style={{
              fontSize: 'var(--text-sm)',
              color: 'var(--gray-600)',
              fontWeight: '500'
            }}>
              Online
            </span>
          </div>
        </div>

        {/* Messages Container */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: 'var(--space-4)',
          background: '#fafbfc'
        }}>
          <div style={{
            maxWidth: '800px',
            margin: '0 auto'
          }}>
            {messages.length === 0 ? (
              // Welcome Screen
              <div style={{
                textAlign: 'center',
                padding: 'var(--space-12) var(--space-4)',
                color: 'var(--gray-600)'
              }}>
                <div style={{
                  width: '80px',
                  height: '80px',
                  background: 'linear-gradient(135deg, var(--primary-brand), var(--primary-light))',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto var(--space-6)'
                }}>
                  <i className="fas fa-shield-alt" style={{ fontSize: '32px', color: 'white' }}></i>
                </div>
                
                <h3 style={{
                  fontSize: 'var(--text-2xl)',
                  fontWeight: '600',
                  color: 'var(--gray-900)',
                  marginBottom: 'var(--space-3)'
                }}>
                  Security AI Assistant Ready
                </h3>
                
                <p style={{
                  fontSize: 'var(--text-base)',
                  color: 'var(--gray-600)',
                  marginBottom: 'var(--space-8)',
                  maxWidth: '500px',
                  margin: '0 auto var(--space-8)'
                }}>
                  I'm here to help protect you from fraud, analyze medical bills, 
                  assist with estate planning, and coordinate family security.
                </p>

                {/* Quick Actions */}
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                  gap: 'var(--space-4)',
                  maxWidth: '600px',
                  margin: '0 auto'
                }}>
                  {[
                    { icon: 'fas fa-exclamation-triangle', text: 'Report suspicious activity', color: 'var(--error-color)' },
                    { icon: 'fas fa-file-medical', text: 'Review medical bill', color: 'var(--accent-color)' },
                    { icon: 'fas fa-scroll', text: 'Estate planning help', color: 'var(--success-color)' },
                    { icon: 'fas fa-family', text: 'Family coordination', color: 'var(--warning-color)' }
                  ].map((action, index) => (
                    <button
                      key={index}
                      onClick={() => setInputMessage(`Help me with: ${action.text}`)}
                      style={{
                        background: 'white',
                        border: `1px solid var(--gray-200)`,
                        borderRadius: 'var(--radius-lg)',
                        padding: 'var(--space-4)',
                        textAlign: 'center',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease',
                        boxShadow: 'var(--shadow-sm)'
                      }}
                    >
                      <i className={action.icon} style={{ 
                        fontSize: '20px', 
                        color: action.color,
                        marginBottom: 'var(--space-2)',
                        display: 'block'
                      }}></i>
                      <span style={{
                        fontSize: 'var(--text-sm)',
                        fontWeight: '500',
                        color: 'var(--gray-700)'
                      }}>
                        {action.text}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              // Chat Messages
              <>
                {messages.map((msg) => (
                  <div key={msg.id} style={{
                    marginBottom: 'var(--space-4)',
                    display: 'flex',
                    justifyContent: msg.type === 'user' ? 'flex-end' : 'flex-start'
                  }}>
                    {msg.type !== 'user' && (
                      <div style={{
                        width: '32px',
                        height: '32px',
                        background: msg.type === 'error' ? 'var(--error-color)' : 'var(--primary-brand)',
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        marginRight: 'var(--space-2)',
                        flexShrink: 0
                      }}>
                        <i className={msg.type === 'error' ? 'fas fa-exclamation' : 'fas fa-robot'} 
                           style={{ fontSize: '14px', color: 'white' }}></i>
                      </div>
                    )}
                    
                    <div style={{
                      maxWidth: '70%',
                      position: 'relative'
                    }}>
                      <div style={{
                        background: msg.type === 'user' ? 'var(--primary-brand)' : 
                                   msg.type === 'error' ? 'var(--error-color)' : 'white',
                        color: msg.type === 'user' || msg.type === 'error' ? 'white' : 'var(--gray-900)',
                        padding: 'var(--space-3) var(--space-4)',
                        borderRadius: msg.type === 'user' ? 
                          'var(--radius-lg) var(--radius-lg) var(--space-1) var(--radius-lg)' :
                          'var(--radius-lg) var(--radius-lg) var(--radius-lg) var(--space-1)',
                        fontSize: 'var(--text-base)',
                        lineHeight: '1.5',
                        boxShadow: msg.type !== 'user' ? 'var(--shadow-sm)' : 'none',
                        border: msg.type !== 'user' ? '1px solid var(--gray-200)' : 'none',
                        whiteSpace: 'pre-wrap'
                      }}>
                        {msg.text}
                      </div>
                      
                      {msg.risk && (
                        <div style={{
                          marginTop: 'var(--space-2)',
                          padding: 'var(--space-1) var(--space-2)',
                          background: msg.risk === 'high' ? 'var(--error-color)' : 
                                      msg.risk === 'medium' ? 'var(--warning-color)' : 'var(--success-color)',
                          color: 'white',
                          borderRadius: 'var(--radius-sm)',
                          fontSize: 'var(--text-xs)',
                          fontWeight: '600',
                          display: 'inline-block'
                        }}>
                          Risk: {msg.risk.toUpperCase()}
                        </div>
                      )}
                      
                      <div style={{
                        fontSize: 'var(--text-xs)',
                        color: 'var(--gray-500)',
                        marginTop: 'var(--space-1)',
                        textAlign: msg.type === 'user' ? 'right' : 'left'
                      }}>
                        {msg.timestamp}
                      </div>
                    </div>
                  </div>
                ))}
                
                {/* Typing Indicator */}
                {isTyping && (
                  <div style={{
                    marginBottom: 'var(--space-4)',
                    display: 'flex',
                    justifyContent: 'flex-start'
                  }}>
                    <div style={{
                      width: '32px',
                      height: '32px',
                      background: 'var(--primary-brand)',
                      borderRadius: '50%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      marginRight: 'var(--space-2)',
                      flexShrink: 0
                    }}>
                      <i className="fas fa-robot" style={{ fontSize: '14px', color: 'white' }}></i>
                    </div>
                    
                    <div style={{
                      background: 'white',
                      padding: 'var(--space-3) var(--space-4)',
                      borderRadius: 'var(--radius-lg) var(--radius-lg) var(--radius-lg) var(--space-1)',
                      border: '1px solid var(--gray-200)',
                      boxShadow: 'var(--shadow-sm)',
                      display: 'flex',
                      alignItems: 'center',
                      gap: 'var(--space-1)'
                    }}>
                      <div style={{
                        width: '8px',
                        height: '8px',
                        background: 'var(--gray-400)',
                        borderRadius: '50%',
                        animation: 'typing 1.4s infinite ease-in-out'
                      }}></div>
                      <div style={{
                        width: '8px',
                        height: '8px',
                        background: 'var(--gray-400)',
                        borderRadius: '50%',
                        animation: 'typing 1.4s infinite ease-in-out',
                        animationDelay: '0.2s'
                      }}></div>
                      <div style={{
                        width: '8px',
                        height: '8px',
                        background: 'var(--gray-400)',
                        borderRadius: '50%',
                        animation: 'typing 1.4s infinite ease-in-out',
                        animationDelay: '0.4s'
                      }}></div>
                    </div>
                  </div>
                )}
              </>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div style={{
          background: 'white',
          borderTop: '1px solid var(--gray-200)',
          padding: 'var(--space-4) var(--space-6)'
        }}>
          <div style={{
            maxWidth: '800px',
            margin: '0 auto',
            display: 'flex',
            gap: 'var(--space-3)',
            alignItems: 'flex-end'
          }}>
            <div style={{
              flex: 1,
              position: 'relative'
            }}>
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about fraud protection, medical bills, estate planning..."
                style={{
                  width: '100%',
                  minHeight: '48px',
                  maxHeight: '120px',
                  padding: 'var(--space-3) var(--space-4)',
                  border: '1px solid var(--gray-300)',
                  borderRadius: 'var(--radius-lg)',
                  fontSize: 'var(--text-base)',
                  fontFamily: 'inherit',
                  resize: 'none',
                  outline: 'none',
                  transition: 'border-color 0.2s ease',
                  backgroundColor: isTyping ? 'var(--gray-50)' : 'white'
                }}
                disabled={isTyping}
                rows="1"
              />
            </div>
            
            <button
              onClick={handleSendMessage}
              disabled={isTyping || !inputMessage.trim()}
              style={{
                background: inputMessage.trim() && !isTyping ? 'var(--primary-brand)' : 'var(--gray-400)',
                color: 'white',
                border: 'none',
                borderRadius: '50%',
                width: '48px',
                height: '48px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: inputMessage.trim() && !isTyping ? 'pointer' : 'not-allowed',
                transition: 'all 0.2s ease'
              }}
            >
              <i className="fas fa-paper-plane" style={{ fontSize: '16px' }}></i>
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Modern Document Upload Interface
  const UploadPage = () => {
    const [dragActive, setDragActive] = useState(false);
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [uploading, setUploading] = useState(false);
    const fileInputRef = useRef(null);

    const handleDrag = (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (e.type === "dragenter" || e.type === "dragover") {
        setDragActive(true);
      } else if (e.type === "dragleave") {
        setDragActive(false);
      }
    };

    const handleDrop = (e) => {
      e.preventDefault();
      e.stopPropagation();
      setDragActive(false);
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleFiles(e.dataTransfer.files);
      }
    };

    const handleChange = (e) => {
      e.preventDefault();
      if (e.target.files && e.target.files[0]) {
        handleFiles(e.target.files);
      }
    };

    const handleFiles = async (files) => {
      setUploading(true);
      const newFiles = [];

      for (let file of files) {
        try {
          await new Promise(resolve => setTimeout(resolve, 1000)); // simulate upload
          newFiles.push({
            id: Date.now() + Math.random(),
            name: file.name,
            size: (file.size / 1024 / 1024).toFixed(2) + ' MB',
            type: file.type,
            uploadTime: new Date().toLocaleString(),
            status: 'completed'
          });
        } catch (error) {
          newFiles.push({
            id: Date.now() + Math.random(),
            name: file.name,
            size: (file.size / 1024 / 1024).toFixed(2) + ' MB',
            type: file.type,
            uploadTime: new Date().toLocaleString(),
            status: 'error'
          });
        }
      }

      setUploadedFiles(prev => [...prev, ...newFiles]);
      setUploading(false);
    };

    const removeFile = (fileId) => {
      setUploadedFiles(prev => prev.filter(file => file.id !== fileId));
    };

    return (
      <div style={{ 
        minHeight: 'calc(100vh - 72px)', 
        background: 'var(--gray-50)', 
        padding: 'var(--space-8) var(--space-6)' 
      }}>
        <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
          
          {/* Header */}
          <div style={{ textAlign: 'center', marginBottom: 'var(--space-12)' }}>
            <div style={{
              width: '64px',
              height: '64px',
              background: 'linear-gradient(135deg, var(--primary-brand), var(--primary-light))',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto var(--space-4)',
              boxShadow: 'var(--shadow-lg)'
            }}>
              <i className="fas fa-upload" style={{ fontSize: '24px', color: 'white' }}></i>
            </div>
            
            <h1 style={{ 
              fontSize: 'var(--text-3xl)', 
              fontWeight: '700', 
              color: 'var(--gray-900)',
              marginBottom: 'var(--space-2)'
            }}>
              Secure Document Upload
            </h1>
            <p style={{ 
              fontSize: 'var(--text-lg)', 
              color: 'var(--gray-600)',
              maxWidth: '500px',
              margin: '0 auto'
            }}>
              Upload financial documents for AI-powered analysis and secure storage
            </p>
          </div>

          {/* Upload Zone */}
          <div className="card" style={{ marginBottom: 'var(--space-8)' }}>
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              style={{
                border: dragActive ? 
                  '2px dashed var(--primary-brand)' : 
                  '2px dashed var(--gray-300)',
                borderRadius: 'var(--radius-lg)',
                padding: 'var(--space-16) var(--space-8)',
                textAlign: 'center',
                background: dragActive ? 
                  'linear-gradient(135deg, rgba(30, 77, 114, 0.05), rgba(37, 99, 235, 0.05))' : 
                  'var(--gray-50)',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
              }}
            >
              <input
                ref={fileInputRef}
                type="file"
                multiple
                onChange={handleChange}
                style={{ display: 'none' }}
                accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.txt,.xls,.xlsx"
              />
              
              <div style={{
                width: '48px',
                height: '48px',
                background: dragActive ? 'var(--primary-brand)' : 'var(--gray-300)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto var(--space-4)',
                transition: 'all 0.3s ease'
              }}>
                <i className="fas fa-cloud-upload-alt" style={{ 
                  fontSize: '20px', 
                  color: dragActive ? 'white' : 'var(--gray-600)' 
                }}></i>
              </div>
              
              {uploading ? (
                <div>
                  <h3 style={{ 
                    fontSize: 'var(--text-lg)', 
                    fontWeight: '600', 
                    color: 'var(--primary-brand)',
                    marginBottom: 'var(--space-2)'
                  }}>
                    Uploading files...
                  </h3>
                  <p style={{ 
                    fontSize: 'var(--text-base)', 
                    color: 'var(--gray-600)' 
                  }}>
                    Please wait while we securely process your documents
                  </p>
                </div>
              ) : (
                <div>
                  <h3 style={{ 
                    fontSize: 'var(--text-lg)', 
                    fontWeight: '600', 
                    color: 'var(--gray-900)',
                    marginBottom: 'var(--space-2)'
                  }}>
                    {dragActive ? 'Drop files here' : 'Upload Documents'}
                  </h3>
                  <p style={{ 
                    fontSize: 'var(--text-base)', 
                    color: 'var(--gray-600)',
                    marginBottom: 'var(--space-3)'
                  }}>
                    Drag and drop files here, or click to browse
                  </p>
                  <p style={{ 
                    fontSize: 'var(--text-sm)', 
                    color: 'var(--gray-500)' 
                  }}>
                    Supports: PDF, DOC, DOCX, JPG, PNG, TXT, XLS, XLSX
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Uploaded Files */}
          {uploadedFiles.length > 0 && (
            <div className="card">
              <div style={{ padding: 'var(--space-6)' }}>
                <h3 style={{ 
                  fontSize: 'var(--text-xl)', 
                  fontWeight: '600',
                  color: 'var(--gray-900)',
                  marginBottom: 'var(--space-4)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 'var(--space-2)'
                }}>
                  <i className="fas fa-file-alt" style={{ color: 'var(--primary-brand)' }}></i>
                  Uploaded Files ({uploadedFiles.length})
                </h3>
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
                  {uploadedFiles.map((file) => (
                    <div key={file.id} style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: 'var(--space-4)',
                      background: 'var(--gray-50)',
                      border: '1px solid var(--gray-200)',
                      borderRadius: 'var(--radius-lg)',
                      transition: 'all 0.2s ease'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                        <div style={{
                          width: '40px',
                          height: '40px',
                          background: file.status === 'completed' ? 'var(--success-color)' : 'var(--error-color)',
                          borderRadius: 'var(--radius-md)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center'
                        }}>
                          <i className={file.status === 'completed' ? 'fas fa-check' : 'fas fa-times'} 
                             style={{ fontSize: '16px', color: 'white' }}></i>
                        </div>
                        
                        <div>
                          <div style={{ 
                            fontWeight: '600', 
                            color: 'var(--gray-900)', 
                            fontSize: 'var(--text-base)',
                            marginBottom: 'var(--space-1)'
                          }}>
                            {file.name}
                          </div>
                          <div style={{ 
                            fontSize: 'var(--text-sm)', 
                            color: 'var(--gray-500)' 
                          }}>
                            {file.size} • {file.uploadTime}
                          </div>
                        </div>
                      </div>
                      
                      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                        <div style={{
                          backgroundColor: file.status === 'completed' ? 'var(--success-color)' : 'var(--error-color)',
                          color: 'white',
                          padding: 'var(--space-1) var(--space-3)',
                          borderRadius: 'var(--radius-lg)',
                          fontSize: 'var(--text-sm)',
                          fontWeight: '600'
                        }}>
                          {file.status === 'completed' ? '✓ Uploaded' : '✗ Failed'}
                        </div>
                        
                        <button
                          onClick={() => removeFile(file.id)}
                          style={{
                            backgroundColor: 'transparent',
                            border: '1px solid var(--error-color)',
                            color: 'var(--error-color)',
                            padding: 'var(--space-2) var(--space-3)',
                            borderRadius: 'var(--radius-md)',
                            fontSize: 'var(--text-sm)',
                            cursor: 'pointer',
                            transition: 'all 0.2s ease'
                          }}
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <>
      <style>{`
        @keyframes typing {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-10px); }
        }
        
        .card:hover {
          transform: translateY(-2px);
        }
        
        input:focus, textarea:focus {
          border-color: var(--primary-brand) !important;
          box-shadow: 0 0 0 3px rgba(30, 77, 114, 0.1) !important;
        }
        
        button:hover:not(:disabled) {
          transform: translateY(-1px);
          box-shadow: var(--shadow-lg);
        }
      `}</style>
      
      <div style={{
        fontFamily: 'Inter, system-ui, -apple-system, sans-serif',
        background: 'var(--gray-50)',
        minHeight: '100vh',
        margin: 0,
        padding: 0
      }}>
        <Navigation />
        
        {currentPage === 'home' && <HomePage />}
        {currentPage === 'chat' && <ChatPage />}
        {currentPage === 'upload' && <UploadPage />}
      </div>
    </>
  );
};

export default WisdomWealthApp;