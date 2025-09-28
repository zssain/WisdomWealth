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
        padding: 'var(--space-4) var(--space-6)',
        height: '72px'
      }}>
        {/* Logo Section */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--space-3)'
        }}>
          <div style={{
            width: '40px',
            height: '40px',
            background: 'var(--primary-brand)',
            color: 'white',
            borderRadius: 'var(--radius-lg)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <i className="fas fa-shield-alt" style={{ fontSize: '18px' }}></i>
          </div>
          <div>
            <h1 style={{
              fontSize: 'var(--text-xl)',
              fontWeight: '600',
              color: 'var(--gray-900)',
              margin: 0,
              lineHeight: 1
            }}>
              WisdomWealth
            </h1>
            <p style={{
              fontSize: 'var(--text-xs)',
              color: 'var(--gray-500)',
              margin: 0,
              lineHeight: 1
            }}>
              Financial Security Platform
            </p>
          </div>
        </div>
        
        {/* Modern Tab Navigation */}
        <div style={{
          display: 'flex',
          background: 'var(--gray-100)',
          borderRadius: 'var(--radius-lg)',
          padding: 'var(--space-1)',
          gap: 'var(--space-1)'
        }}>
          {[
            { id: 'home', icon: 'fas fa-home', label: 'Dashboard' },
            { id: 'chat', icon: 'fas fa-comments', label: 'Security Chat' },
            { id: 'upload', icon: 'fas fa-cloud-upload-alt', label: 'Documents' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setCurrentPage(tab.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--space-2)',
                padding: 'var(--space-2) var(--space-4)',
                background: currentPage === tab.id ? 'white' : 'transparent',
                color: currentPage === tab.id ? 'var(--primary-brand)' : 'var(--gray-600)',
                border: 'none',
                borderRadius: 'var(--radius-md)',
                fontSize: 'var(--text-sm)',
                fontWeight: currentPage === tab.id ? '600' : '500',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                boxShadow: currentPage === tab.id ? 'var(--shadow-sm)' : 'none'
              }}
            >
              <i className={tab.icon} style={{ fontSize: '14px' }}></i>
              {tab.label}
            </button>
          ))}
        </div>

        {/* Status Indicator */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--space-2)',
          padding: 'var(--space-2) var(--space-3)',
          background: 'var(--gray-50)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--gray-200)'
        }}>
          <div style={{
            width: '8px',
            height: '8px',
            background: 'var(--success-color)',
            borderRadius: '50%'
          }}></div>
          <span style={{
            fontSize: 'var(--text-xs)',
            color: 'var(--gray-600)',
            fontWeight: '500'
          }}>
            Secure Connection
          </span>
        </div>
      </div>
    </nav>
  );

  // Professional Dashboard Homepage
  const HomePage = () => (
    <div style={{ 
      background: 'var(--gray-50)', 
      minHeight: 'calc(100vh - 72px)'
    }}>
      {/* Hero Dashboard Section */}
      <div style={{
        background: 'linear-gradient(135deg, var(--primary-brand) 0%, #2563eb 100%)',
        padding: 'var(--space-12) 0 var(--space-16)'
      }}>
        <div style={{
          maxWidth: '1400px',
          margin: '0 auto',
          padding: '0 var(--space-6)'
        }}>
          <div style={{
            background: 'white',
            borderRadius: 'var(--radius-xl)',
            boxShadow: 'var(--shadow-lg)',
            padding: 'var(--space-12) var(--space-8)',
            textAlign: 'center'
          }}>
            <div style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 'var(--space-3)',
              background: 'var(--gray-50)',
              padding: 'var(--space-2) var(--space-4)',
              borderRadius: 'var(--radius-lg)',
              marginBottom: 'var(--space-6)'
            }}>
              <div style={{
                width: '24px',
                height: '24px',
                background: 'var(--success-color)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <i className="fas fa-check" style={{ fontSize: '12px', color: 'white' }}></i>
              </div>
              <span style={{
                fontSize: 'var(--text-sm)',
                fontWeight: '600',
                color: 'var(--gray-700)'
              }}>
                Enterprise-Grade Security Active
              </span>
            </div>
            
            <h1 style={{
              fontSize: 'var(--text-4xl)',
              fontWeight: '700',
              color: 'var(--gray-900)',
              marginBottom: 'var(--space-4)',
              lineHeight: '1.1'
            }}>
              Financial Security
              <br />
              <span style={{ color: 'var(--primary-brand)' }}>
                Intelligence Platform
              </span>
            </h1>
            
            <p style={{
              fontSize: 'var(--text-lg)',
              color: 'var(--gray-600)',
              maxWidth: '600px',
              margin: '0 auto var(--space-8)',
              lineHeight: '1.6'
            }}>
              Advanced AI-powered protection against fraud, healthcare billing optimization, 
              estate planning automation, and secure family coordination.
            </p>

            <div style={{
              display: 'flex',
              justifyContent: 'center',
              gap: 'var(--space-4)',
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
                  fontSize: 'var(--text-base)',
                  fontWeight: '600',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 'var(--space-2)',
                  transition: 'all 0.2s ease'
                }}
              >
                <i className="fas fa-shield-alt"></i>
                Start Security Analysis
              </button>
              <button 
                onClick={() => setCurrentPage('upload')}
                style={{
                  background: 'white',
                  color: 'var(--primary-brand)',
                  border: '2px solid var(--primary-brand)',
                  padding: 'var(--space-3) var(--space-6)',
                  borderRadius: 'var(--radius-lg)',
                  fontSize: 'var(--text-base)',
                  fontWeight: '600',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 'var(--space-2)',
                  transition: 'all 0.2s ease'
                }}
              >
                <i className="fas fa-cloud-upload-alt"></i>
                Upload Documents
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Security Services Grid */}
      <div style={{
        padding: 'var(--space-16) 0',
        background: 'white'
      }}>
        <div style={{
          maxWidth: '1400px',
          margin: '0 auto',
          padding: '0 var(--space-6)'
        }}>
          <div style={{
            textAlign: 'center',
            marginBottom: 'var(--space-12)'
          }}>
            <h2 style={{
              fontSize: 'var(--text-3xl)',
              fontWeight: '700',
              color: 'var(--gray-900)',
              marginBottom: 'var(--space-4)'
            }}>
              Comprehensive Financial Protection
            </h2>
            <p style={{
              fontSize: 'var(--text-lg)',
              color: 'var(--gray-600)',
              maxWidth: '600px',
              margin: '0 auto'
            }}>
              Four specialized AI agents working together to protect your financial security
            </p>
          </div>

          <div className="grid grid-cols-4" style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: 'var(--space-6)'
          }}>
            {serviceCards.map((service, index) => (
              <div
                key={index}
                className="card"
                style={{
                  background: 'white',
                  border: '1px solid var(--gray-200)',
                  borderRadius: 'var(--radius-xl)',
                  padding: 'var(--space-6)',
                  boxShadow: 'var(--shadow-sm)',
                  transition: 'all 0.2s ease',
                  cursor: 'pointer',
                  height: '100%'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-4px)';
                  e.currentTarget.style.boxShadow = 'var(--shadow-lg)';
                  e.currentTarget.style.borderColor = service.color;
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
                  e.currentTarget.style.borderColor = 'var(--gray-200)';
                }}
                onClick={() => setCurrentPage('chat')}
              >
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  marginBottom: 'var(--space-4)'
                }}>
                  <div style={{
                    width: '48px',
                    height: '48px',
                    background: service.bgColor,
                    borderRadius: 'var(--radius-lg)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginRight: 'var(--space-4)'
                  }}>
                    <i className={service.icon} style={{
                      fontSize: '20px',
                      color: service.color
                    }}></i>
                  </div>
                  <div style={{
                    width: '12px',
                    height: '12px',
                    background: 'var(--success-color)',
                    borderRadius: '50%',
                    marginLeft: 'auto'
                  }}></div>
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
                  fontSize: 'var(--text-sm)',
                  color: 'var(--gray-600)',
                  lineHeight: '1.5',
                  marginBottom: 'var(--space-4)'
                }}>
                  {service.description}
                </p>

                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  paddingTop: 'var(--space-4)',
                  borderTop: '1px solid var(--gray-100)'
                }}>
                  <span style={{
                    fontSize: 'var(--text-sm)',
                    fontWeight: '600',
                    color: service.color
                  }}>
                    Access Agent
                  </span>
                  <i className="fas fa-arrow-right" style={{
                    fontSize: '14px',
                    color: service.color
                  }}></i>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Security Metrics & Trust Indicators */}
      <div style={{
        padding: 'var(--space-16) 0',
        background: 'var(--gray-50)'
      }}>
        <div style={{
          maxWidth: '1400px',
          margin: '0 auto',
          padding: '0 var(--space-6)'
        }}>
          {/* Stats Grid */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: 'var(--space-6)',
            marginBottom: 'var(--space-12)'
          }}>
            {[
              {
                icon: 'fas fa-shield-check',
                number: '99.9%',
                label: 'Threat Detection Rate',
                description: 'Advanced AI identifies suspicious patterns',
                color: 'var(--success-color)'
              },
              {
                icon: 'fas fa-users-shield',
                number: '50K+',
                label: 'Protected Families',
                description: 'Seniors trust our security platform',
                color: 'var(--primary-brand)'
              },
              {
                icon: 'fas fa-clock',
                number: '< 2min',
                label: 'Response Time',
                description: 'Real-time fraud detection alerts',
                color: 'var(--accent-color)'
              },
              {
                icon: 'fas fa-award',
                number: '256-bit',
                label: 'Encryption Standard',
                description: 'Bank-grade security protocols',
                color: 'var(--warning-color)'
              }
            ].map((stat, index) => (
              <div
                key={index}
                style={{
                  background: 'white',
                  borderRadius: 'var(--radius-xl)',
                  padding: 'var(--space-6)',
                  border: '1px solid var(--gray-200)',
                  boxShadow: 'var(--shadow-sm)',
                  textAlign: 'center'
                }}
              >
                <div style={{
                  width: '56px',
                  height: '56px',
                  background: `${stat.color}15`,
                  borderRadius: 'var(--radius-lg)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto var(--space-4)'
                }}>
                  <i className={stat.icon} style={{
                    fontSize: '24px',
                    color: stat.color
                  }}></i>
                </div>
                
                <div style={{
                  fontSize: 'var(--text-3xl)',
                  fontWeight: '700',
                  color: 'var(--gray-900)',
                  marginBottom: 'var(--space-2)'
                }}>
                  {stat.number}
                </div>
                
                <div style={{
                  fontSize: 'var(--text-base)',
                  fontWeight: '600',
                  color: 'var(--gray-700)',
                  marginBottom: 'var(--space-2)'
                }}>
                  {stat.label}
                </div>
                
                <div style={{
                  fontSize: 'var(--text-sm)',
                  color: 'var(--gray-500)',
                  lineHeight: '1.5'
                }}>
                  {stat.description}
                </div>
              </div>
            ))}
          </div>

          {/* Trust Badges */}
          <div style={{
            background: 'white',
            borderRadius: 'var(--radius-xl)',
            padding: 'var(--space-8)',
            border: '1px solid var(--gray-200)',
            boxShadow: 'var(--shadow-sm)',
            textAlign: 'center'
          }}>
            <h3 style={{
              fontSize: 'var(--text-xl)',
              fontWeight: '600',
              color: 'var(--gray-900)',
              marginBottom: 'var(--space-6)'
            }}>
              Trusted by Security Professionals
            </h3>
            
            <div style={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              gap: 'var(--space-8)',
              flexWrap: 'wrap'
            }}>
              {[
                { icon: 'fas fa-university', label: 'FDIC Compliant' },
                { icon: 'fas fa-certificate', label: 'SOC 2 Certified' },
                { icon: 'fas fa-lock', label: 'HIPAA Secure' },
                { icon: 'fas fa-check-circle', label: 'PCI DSS Level 1' }
              ].map((badge, index) => (
                <div key={index} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 'var(--space-2)',
                  color: 'var(--gray-600)'
                }}>
                  <i className={badge.icon} style={{ fontSize: '18px' }}></i>
                  <span style={{
                    fontSize: 'var(--text-sm)',
                    fontWeight: '500'
                  }}>
                    {badge.label}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
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
        const response = await fetch('http://localhost:8000/route', {
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
              width: '48px',
              height: '48px',
              background: 'linear-gradient(135deg, var(--primary-brand), var(--primary-light))',
              borderRadius: 'var(--radius-lg)',
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
                      
                      {/* Message metadata */}
                      <div style={{
                        display: 'flex',
                        justifyContent: msg.type === 'user' ? 'flex-end' : 'flex-start',
                        alignItems: 'center',
                        gap: 'var(--space-2)',
                        marginTop: 'var(--space-1)',
                        padding: '0 var(--space-1)'
                      }}>
                        <span style={{
                          fontSize: 'var(--text-xs)',
                          color: 'var(--gray-400)'
                        }}>
                          {msg.timestamp}
                        </span>
                        
                        {msg.risk && (
                          <span style={{
                            background: msg.risk === 'HIGH' ? 'var(--error-color)' : 
                                       msg.risk === 'MEDIUM' ? 'var(--warning-color)' : 'var(--success-color)',
                            color: 'white',
                            padding: '2px 8px',
                            borderRadius: 'var(--radius-sm)',
                            fontSize: 'var(--text-xs)',
                            fontWeight: '500'
                          }}>
                            {msg.risk}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </>
            )}
            
            {/* Typing Indicator */}
            {isTyping && (
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--space-2)',
                marginBottom: 'var(--space-4)'
              }}>
                <div style={{
                  width: '32px',
                  height: '32px',
                  background: 'var(--primary-brand)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <i className="fas fa-robot" style={{ fontSize: '14px', color: 'white' }}></i>
                </div>
                <div style={{
                  background: 'white',
                  padding: 'var(--space-3) var(--space-4)',
                  borderRadius: 'var(--radius-lg)',
                  border: '1px solid var(--gray-200)',
                  boxShadow: 'var(--shadow-sm)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 'var(--space-2)'
                }}>
                  <div className="typing-dots" style={{
                    display: 'flex',
                    gap: '4px'
                  }}>
                    {[1, 2, 3].map(dot => (
                      <div key={dot} style={{
                        width: '6px',
                        height: '6px',
                        background: 'var(--gray-400)',
                        borderRadius: '50%',
                        animation: `typing 1.4s infinite ease-in-out ${dot * 0.2}s`
                      }}></div>
                    ))}
                  </div>
                  <span style={{
                    fontSize: 'var(--text-sm)',
                    color: 'var(--gray-500)',
                    fontStyle: 'italic'
                  }}>
                    Analyzing...
                  </span>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Modern Input Bar */}
        <div style={{
          background: 'white',
          borderTop: '1px solid var(--gray-200)',
          padding: 'var(--space-4) var(--space-6)'
        }}>
          <div style={{
            maxWidth: '800px',
            margin: '0 auto',
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-3)'
          }}>
            <div style={{
              flex: 1,
              position: 'relative'
            }}>
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about suspicious calls, medical bills, or financial security..."
                disabled={isTyping}
                style={{
                  width: '100%',
                  padding: 'var(--space-3) var(--space-4)',
                  paddingRight: 'var(--space-12)',
                  border: '1px solid var(--gray-300)',
                  borderRadius: 'var(--radius-xl)',
                  fontSize: 'var(--text-base)',
                  outline: 'none',
                  background: 'var(--gray-50)',
                  transition: 'all 0.2s ease'
                }}
              />
              <button
                onClick={handleSendMessage}
                disabled={isTyping || !inputMessage.trim()}
                style={{
                  position: 'absolute',
                  right: 'var(--space-2)',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: inputMessage.trim() && !isTyping ? 'var(--primary-brand)' : 'var(--gray-400)',
                  color: 'white',
                  border: 'none',
                  borderRadius: '50%',
                  width: '32px',
                  height: '32px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: inputMessage.trim() && !isTyping ? 'pointer' : 'not-allowed',
                  transition: 'all 0.2s ease'
                }}
              >
                <i className="fas fa-paper-plane" style={{ fontSize: '14px' }}></i>
              </button>
            </div>
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
      <div style={{ minHeight: 'calc(100vh - 72px)', background: 'var(--gray-50)', padding: '40px 20px' }}>
        <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
          
          {/* Header */}
          <div style={{ textAlign: 'center', marginBottom: '32px' }}>
            <h1 style={{ fontSize: '2em', fontWeight: '700', color: '#2c3e50' }}>
              Secure Document Upload
            </h1>
            <p style={{ fontSize: '1.1em', color: '#6c757d' }}>
              Upload financial documents for AI-powered analysis
            </p>
          </div>

          {/* Upload Zone */}
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            style={{
              border: dragActive ? '2px dashed #1e4d72' : '2px dashed #ccc',
              borderRadius: '12px',
              padding: '60px 30px',
              textAlign: 'center',
              marginBottom: '32px',
              background: dragActive ? '#f8f9fc' : '#fff',
              cursor: 'pointer',
            }}
          >
            <input
              ref={fileInputRef}
              type="file"
              multiple
              onChange={handleChange}
              style={{ display: 'none' }}
              accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.txt"
            />
            {uploading ? (
              <p style={{ fontWeight: '600', color: '#2c3e50' }}>Uploading...</p>
            ) : (
              <p style={{ fontWeight: '600', color: '#2c3e50' }}>Drop files here or click to browse</p>
            )}
          </div>

          {/* Uploaded Files */}
          {uploadedFiles.length > 0 && (
            <div>
              <h3 style={{ fontWeight: '600', marginBottom: '16px' }}>
                Uploaded Files ({uploadedFiles.length})
              </h3>
              {uploadedFiles.map((file) => (
                <div key={file.id} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  padding: '12px',
                  background: '#fff',
                  border: '1px solid #ddd',
                  borderRadius: '8px',
                  marginBottom: '8px'
                }}>
                  <div>
                    <strong>{file.name}</strong> <br />
                    <small>{file.size} • {file.uploadTime}</small>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{
                      background: file.status === 'completed' ? '#27ae60' : '#e74c3c',
                      color: 'white',
                      padding: '4px 8px',
                      borderRadius: '6px',
                      fontSize: '0.8em'
                    }}>
                      {file.status}
                    </span>
                    <button onClick={() => removeFile(file.id)} style={{
                      border: 'none',
                      background: 'transparent',
                      color: '#e74c3c',
                      cursor: 'pointer'
                    }}>✕</button>
                  </div>
                </div>
              ))}
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
        
        input:focus {
          border-color: var(--primary-brand) !important;
          box-shadow: 0 0 0 3px rgba(30, 77, 114, 0.1) !important;
        }
      `}</style>
      
      <div style={{
              textAlign: 'center',
              marginTop: '100px',
              color: '#6c757d'
            }}>
              <div style={{ fontSize: '60px', marginBottom: '20px' }}>🤖</div>
              <h3 style={{ fontSize: '1.5em', marginBottom: '15px', color: '#2c3e50' }}>
                Welcome to WisdomWealth Security!
              </h3>
              <p style={{ fontSize: '1.1em', marginBottom: '30px' }}>
                I'm here to help protect you from scams, understand medical bills, and manage your finances safely.
              </p>
              
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '15px',
                marginTop: '30px',
                maxWidth: '800px',
                margin: '30px auto 0'
              }}>
                {[
                  { emoji: '�️', title: 'Fraud Protection', text: 'Report suspicious calls or emails' },
                  { emoji: '💚', title: 'Healthcare Finance', text: 'Get help with medical bills' },
                  { emoji: '📋', title: 'Estate Planning', text: 'Organize important documents' },
                  { emoji: '👥', title: 'Family Alerts', text: 'Keep family informed safely' }
                ].map((card, index) => (
                  <div key={index} style={{
                    backgroundColor: 'white',
                    padding: '20px',
                    borderRadius: '12px',
                    border: '1px solid #e2e8f0',
                    textAlign: 'center',
                    cursor: 'pointer',
                    transition: 'all 0.3s'
                  }}
                  onClick={() => setInputMessage(`Tell me about ${card.title.toLowerCase()}`)}
                  onMouseEnter={(e) => e.target.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)'}
                  onMouseLeave={(e) => e.target.style.boxShadow = 'none'}
                  >
                    <div style={{ fontSize: '30px', marginBottom: '8px' }}>{card.emoji}</div>
                    <div style={{ fontSize: '1em', fontWeight: '600', color: '#2c3e50', marginBottom: '5px' }}>
                      {card.title}
                    </div>
                    <div style={{ fontSize: '0.9em', color: '#6c757d' }}>
                      {card.text}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg) => (
              <div key={msg.id} style={{
                marginBottom: '20px',
                display: 'flex',
                justifyContent: msg.type === 'user' ? 'flex-end' : 'flex-start'
              }}>
                <div style={{
                  backgroundColor: msg.type === 'user' ? '#1e4d72' : 
                                 msg.type === 'error' ? '#e74c3c' : 'white',
                  color: msg.type === 'user' || msg.type === 'error' ? 'white' : '#2c3e50',
                  padding: '16px 20px',
                  borderRadius: '16px',
                  maxWidth: '70%',
                  boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
                  border: msg.type === 'agent' ? '1px solid #e2e8f0' : 'none'
                }}>
                  <div style={{ fontSize: '1em', lineHeight: '1.5', marginBottom: '8px' }}>
                    {msg.text}
                  </div>
                  {msg.risk && (
                    <div style={{
                      fontSize: '0.85em',
                      padding: '6px 12px',
                      backgroundColor: msg.risk === 'high' ? '#e74c3c' : 
                                      msg.risk === 'medium' ? '#f39c12' : '#27ae60',
                      color: 'white',
                      borderRadius: '12px',
                      display: 'inline-block',
                      marginTop: '8px'
                    }}>
                      Risk Level: {msg.risk.toUpperCase()}
                    </div>
                  )}
                  <div style={{
                    fontSize: '0.8em',
                    opacity: 0.7,
                    marginTop: '8px'
                  }}>
                    {msg.timestamp}
                  </div>
                </div>
              </div>
            ))
          )}
          {isTyping && (
            <div style={{
              display: 'flex',
              justifyContent: 'flex-start',
              marginBottom: '20px'
            }}>
              <div style={{
                backgroundColor: 'white',
                padding: '16px 20px',
                borderRadius: '16px',
                boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
                border: '1px solid #e2e8f0'
              }}>
                <div style={{ fontSize: '1em', color: '#6c757d' }}>🤖 Analyzing your request...</div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div style={{
          padding: '20px',
          backgroundColor: 'white',
          borderTop: '1px solid #e2e8f0',
          width: '100%'
        }}>
          <div style={{
            maxWidth: '1200px',
            margin: '0 auto',
            display: 'flex',
            gap: '15px'
          }}>
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about suspicious calls, medical bills, or any financial concerns..."
              style={{
                flex: 1,
                padding: '16px 20px',
                borderRadius: '12px',
                border: '2px solid #e2e8f0',
                fontSize: '1.1em',
                outline: 'none'
              }}
              disabled={isTyping}
            />
            <button
              onClick={handleSendMessage}
              disabled={isTyping || !inputMessage.trim()}
              style={{
                backgroundColor: '#1e4d72',
                color: 'white',
                border: 'none',
                padding: '16px 24px',
                borderRadius: '12px',
                fontSize: '1.1em',
                fontWeight: '600',
                cursor: isTyping || !inputMessage.trim() ? 'not-allowed' : 'pointer',
                opacity: isTyping || !inputMessage.trim() ? 0.6 : 1
              }}
            >
              Send
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
          // Simulate upload process
          await new Promise(resolve => setTimeout(resolve, 1000));
          
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
        <div style={{
          maxWidth: '1000px',
          margin: '0 auto'
        }}>
          {/* Header */}
          <div style={{
            textAlign: 'center',
            marginBottom: 'var(--space-8)'
          }}>
            <h1 style={{
              fontSize: 'var(--text-3xl)',
              fontWeight: '700',
              color: 'var(--gray-900)',
              marginBottom: 'var(--space-3)'
            }}>
              Secure Document Upload
            </h1>
            <p style={{
              fontSize: 'var(--text-lg)',
              color: 'var(--gray-600)',
              maxWidth: '600px',
              margin: '0 auto'
            }}>
              Upload your financial documents for AI-powered security analysis and protection guidance
            </p>
          </div>

          {/* Upload Zone */}
          <div
            style={{
              background: 'white',
              border: dragActive ? '2px dashed var(--primary-brand)' : '2px dashed var(--gray-300)',
              borderRadius: 'var(--radius-xl)',
              padding: 'var(--space-12)',
              textAlign: 'center',
              marginBottom: 'var(--space-8)',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              backgroundColor: dragActive ? 'var(--gray-50)' : 'white'
            }}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              multiple
              onChange={handleChange}
              style={{ display: 'none' }}
              accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.txt"
            />
            
            {uploading ? (
              <div>
                <div style={{
                  width: '64px',
                  height: '64px',
                  background: 'var(--primary-brand)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto var(--space-4)'
                }}>
                  <i className="fas fa-spinner fa-spin" style={{ fontSize: '24px', color: 'white' }}></i>
                </div>
                <p style={{
                  fontSize: 'var(--text-lg)',
                  fontWeight: '600',
                  color: 'var(--gray-700)',
                  margin: 0
                }}>
                  Processing documents...
                </p>
              </div>
            ) : (
              <div>
                <div style={{
                  width: '64px',
                  height: '64px',
                  background: 'var(--gray-100)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto var(--space-4)'
                }}>
                  <i className="fas fa-cloud-upload-alt" style={{ 
                    fontSize: '24px', 
                    color: 'var(--gray-500)' 
                  }}></i>
                </div>
                
                <h3 style={{
                  fontSize: 'var(--text-xl)',
                  fontWeight: '600',
                  color: 'var(--gray-900)',
                  marginBottom: 'var(--space-2)'
                }}>
                  Drop files here or click to browse
                </h3>
                
                <p style={{
                  fontSize: 'var(--text-base)',
                  color: 'var(--gray-600)',
                  marginBottom: 'var(--space-4)'
                }}>
                  Support for PDF, Word, images, and text files
                </p>
                
                <div style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 'var(--space-2)',
                  padding: 'var(--space-2) var(--space-3)',
                  background: 'var(--gray-100)',
                  borderRadius: 'var(--radius-md)',
                  fontSize: 'var(--text-sm)',
                  color: 'var(--gray-600)'
                }}>
                  <i className="fas fa-shield-alt" style={{ fontSize: '12px' }}></i>
                  End-to-end encrypted
                </div>
              </div>
            )}
          </div>

          {/* File Categories */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: 'var(--space-4)',
            marginBottom: 'var(--space-8)'
          }}>
            {[
              { icon: 'fas fa-file-medical', title: 'Medical Bills', desc: 'Insurance claims, hospital invoices' },
              { icon: 'fas fa-university', title: 'Bank Statements', desc: 'Account summaries, transactions' },
              { icon: 'fas fa-file-contract', title: 'Legal Documents', desc: 'Contracts, wills, policies' },
              { icon: 'fas fa-exclamation-triangle', title: 'Suspicious Content', desc: 'Potential scams, fraud attempts' }
            ].map((category, index) => (
              <div key={index} style={{
                background: 'white',
                padding: 'var(--space-4)',
                borderRadius: 'var(--radius-lg)',
                border: '1px solid var(--gray-200)',
                textAlign: 'center'
              }}>
                <i className={category.icon} style={{
                  fontSize: '24px',
                  color: 'var(--primary-brand)',
                  marginBottom: 'var(--space-2)',
                  display: 'block'
                }}></i>
                <div style={{
                  fontSize: 'var(--text-sm)',
                  fontWeight: '600',
                  color: 'var(--gray-900)',
                  marginBottom: 'var(--space-1)'
                }}>
                  {category.title}
                </div>
                <div style={{
                  fontSize: 'var(--text-xs)',
                  color: 'var(--gray-500)'
                }}>
                  {category.desc}
                </div>
              </div>
            ))}
          </div>

          {/* Uploaded Files List */}
          {uploadedFiles.length > 0 && (
            <div style={{
              background: 'white',
              borderRadius: 'var(--radius-xl)',
              padding: 'var(--space-6)',
              border: '1px solid var(--gray-200)'
            }}>
              <h3 style={{
                fontSize: 'var(--text-lg)',
                fontWeight: '600',
                color: 'var(--gray-900)',
                marginBottom: 'var(--space-4)',
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--space-2)'
              }}>
                <i className="fas fa-folder-open" style={{ color: 'var(--primary-brand)' }}></i>
                Uploaded Files ({uploadedFiles.length})
              </h3>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
                {uploadedFiles.map((file) => (
                  <div key={file.id} style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: 'var(--space-3) var(--space-4)',
                    background: 'var(--gray-50)',
                    borderRadius: 'var(--radius-lg)',
                    border: '1px solid var(--gray-200)'
                  }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 'var(--space-3)',
                      flex: 1
                    }}>
                      <i className="fas fa-file" style={{ 
                        color: 'var(--gray-400)', 
                        fontSize: '16px' 
                      }}></i>
                      <div>
                        <div style={{
                          fontWeight: '500',
                          color: 'var(--gray-900)',
                          fontSize: 'var(--text-sm)'
                        }}>
                          {file.name}
                        </div>
                        <div style={{
                          fontSize: 'var(--text-xs)',
                          color: 'var(--gray-500)'
                        }}>
                          {file.size} • {file.uploadTime}
                        </div>
                      </div>
                    </div>
                    
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 'var(--space-3)'
                    }}>
                      <span style={{
                        background: file.status === 'completed' ? 'var(--success-color)' : 'var(--error-color)',
                        color: 'white',
                        padding: '4px 8px',
                        borderRadius: 'var(--radius-sm)',
                        fontSize: 'var(--text-xs)',
                        fontWeight: '500'
                      }}>
                        {file.status === 'completed' ? 'Uploaded' : 'Failed'}
                      </span>
                      
                      <button
                        onClick={() => removeFile(file.id)}
                        style={{
                          background: 'transparent',
                          border: 'none',
                          color: 'var(--gray-400)',
                          cursor: 'pointer',
                          padding: 'var(--space-1)',
                          borderRadius: 'var(--radius-sm)'
                        }}
                      >
                        <i className="fas fa-times"></i>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (

    const handleFiles = async (files) => {
      setUploading(true);
      const newFiles = [];
      
      for (let file of files) {
        try {
          // Simulate upload process - replace with actual upload logic
          await new Promise(resolve => setTimeout(resolve, 1000));
          
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
            status: 'error',
            error: 'Upload failed'
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
        width: '100%',
        minHeight: 'calc(100vh - 80px)',
        backgroundColor: '#f8f9fa',
        padding: '40px 20px'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto'
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '24px',
            padding: '60px',
            boxShadow: '0 12px 40px rgba(0,0,0,0.1)',
            textAlign: 'center'
          }}>
            <h2 style={{
              fontSize: '2.8em',
              fontWeight: 'bold',
              color: '#2c3e50',
              marginBottom: '20px'
            }}>
              📄 Document Upload
            </h2>
            <p style={{
              fontSize: '1.3em',
              color: '#6c757d',
              marginBottom: '50px',
              maxWidth: '600px',
              margin: '0 auto 50px'
            }}>
              Securely upload your financial documents for analysis and protection advice from your AI security team
            </p>

            {/* Upload Area */}
            <div
              style={{
                border: dragActive ? '3px dashed #1e4d72' : '2px dashed #ccc',
                borderRadius: '20px',
                padding: '80px 40px',
                marginBottom: '40px',
                backgroundColor: dragActive ? '#f8f9fc' : '#fafafa',
                cursor: 'pointer',
                transition: 'all 0.3s',
                position: 'relative'
              }}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                multiple
                onChange={handleChange}
                style={{ display: 'none' }}
                accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.txt"
              />
              
              {uploading ? (
                <div>
                  <div style={{ fontSize: '60px', marginBottom: '20px' }}>⏳</div>
                  <p style={{ fontSize: '1.4em', fontWeight: '600', color: '#2c3e50', margin: '15px 0' }}>
                    Uploading files...
                  </p>
                </div>
              ) : (
                <div>
                  <div style={{ fontSize: '60px', marginBottom: '20px' }}>📄</div>
                  <p style={{ fontSize: '1.4em', fontWeight: '600', color: '#2c3e50', margin: '15px 0' }}>
                    Drop files here or click to browse
                  </p>
                  <p style={{ fontSize: '1.1em', color: '#6c757d' }}>
                    Supports PDF, Word documents, images, and text files
                  </p>
                  <p style={{ fontSize: '0.9em', color: '#6c757d', marginTop: '15px' }}>
                    Your documents are encrypted and secure
                  </p>
                </div>
              )}
            </div>

            {/* File Type Examples */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '20px',
              marginBottom: '40px'
            }}>
              {[
                { icon: '🏥', title: 'Medical Bills', desc: 'Hospital invoices, insurance claims' },
                { icon: '🏛️', title: 'Bank Statements', desc: 'Monthly statements, transactions' },
                { icon: '📜', title: 'Legal Documents', desc: 'Contracts, wills, insurance policies' },
                { icon: '📧', title: 'Suspicious Emails', desc: 'Potential scams or fraud attempts' }
              ].map((type, index) => (
                <div key={index} style={{
                  backgroundColor: '#f8f9fc',
                  padding: '20px',
                  borderRadius: '12px',
                  border: '1px solid #e2e8f0'
                }}>
                  <div style={{ fontSize: '30px', marginBottom: '10px' }}>{type.icon}</div>
                  <div style={{ fontSize: '1em', fontWeight: '600', color: '#2c3e50', marginBottom: '5px' }}>
                    {type.title}
                  </div>
                  <div style={{ fontSize: '0.9em', color: '#6c757d' }}>
                    {type.desc}
                  </div>
                </div>
              ))}
            </div>

            {/* Uploaded Files List */}
            {uploadedFiles.length > 0 && (
              <div style={{
                textAlign: 'left',
                backgroundColor: '#f8f9fc',
                borderRadius: '16px',
                padding: '30px',
                marginTop: '40px'
              }}>
                <h3 style={{
                  fontSize: '1.4em',
                  fontWeight: 'bold',
                  color: '#2c3e50',
                  marginBottom: '20px',
                  textAlign: 'center'
                }}>
                  📁 Uploaded Files ({uploadedFiles.length})
                </h3>
                <div style={{
                  display: 'grid',
                  gap: '15px'
                }}>
                  {uploadedFiles.map((file) => (
                    <div key={file.id} style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '15px 20px',
                      backgroundColor: 'white',
                      borderRadius: '12px',
                      border: '1px solid #e2e8f0',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
                    }}>
                      <div style={{ flex: 1 }}>
                        <div style={{ 
                          fontWeight: '600', 
                          color: '#2c3e50', 
                          fontSize: '1.1em',
                          marginBottom: '5px'
                        }}>
                          📄 {file.name}
                        </div>
                        <div style={{ fontSize: '0.9em', color: '#6c757d' }}>
                          {file.size} • {file.uploadTime}
                        </div>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        <div style={{
                          backgroundColor: file.status === 'completed' ? '#27ae60' : '#e74c3c',
                          color: 'white',
                          padding: '8px 16px',
                          borderRadius: '20px',
                          fontSize: '0.9em',
                          fontWeight: '600'
                        }}>
                          {file.status === 'completed' ? '✓ Uploaded' : '✗ Failed'}
                        </div>
                        <button
                          onClick={() => removeFile(file.id)}
                          style={{
                            backgroundColor: 'transparent',
                            border: '1px solid #e74c3c',
                            color: '#e74c3c',
                            padding: '8px 12px',
                            borderRadius: '8px',
                            fontSize: '0.9em',
                            cursor: 'pointer'
                          }}
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
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
        
        input:focus {
          border-color: var(--primary-brand) !important;
          box-shadow: 0 0 0 3px rgba(30, 77, 114, 0.1) !important;
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
